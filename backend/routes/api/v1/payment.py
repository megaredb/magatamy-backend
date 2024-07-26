import hashlib
import hmac
import uuid
from datetime import datetime
from json import dumps
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from httpx import post, HTTPError, Response as HTTPXResponse
from mctools import RCONClient
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from backend import crud
from backend import schemas
from backend.models import Product, User
from backend.routes.api import deps
from backend.routes.api.v1.discord import auth_middleware
from backend.schemas import payment, UserUpdate
from backend.schemas.payment import PaymentProvider
from backend.schemas.payment.enot import InvoiceCreateResponse
from backend.utils import config
from backend.utils.config import (
    MAIN_MC_SERVER_RCON_HOST,
    MAIN_MC_SERVER_RCON_PORT,
    MAIN_MC_SERVER_RCON_PASSWORD,
)
from backend.utils.product import ProductOperation

router = APIRouter(prefix="/payment", tags=["payment"])


def process_product_purchase(
    db: Session, user: User, product: Product, username: str | None = None
):
    match ProductOperation(product.operation):
        case ProductOperation.TICKET_ACCESS:
            form = crud.form.get(db, product.connected_form_id)

            crud.user.add_purchased_form(db, user, form)
        case ProductOperation.CUSTOM_COMMAND:
            if not username:
                raise HTTPException(400, "Username field not provided.")

            with RCONClient(
                MAIN_MC_SERVER_RCON_HOST,
                MAIN_MC_SERVER_RCON_PORT,
                timeout=10,
            ) as rcon_client:
                if (
                    not rcon_client.login(MAIN_MC_SERVER_RCON_PASSWORD)
                    or not rcon_client.is_connected()
                ):
                    raise HTTPException(500, "Unable to connect to Minecraft server.")

                rcon_client.command(str(product.custom_command).format(player=username))


async def process_value_purchase(db: Session, user: User, value: int):
    crud.user.update(db=db, db_obj=user, obj_in=UserUpdate(money=user.money + value))


# def process_product_refund(db: Session, user: User, product: Product):
#     match ProductOperation(product.operation):
#         case ProductOperation.TICKET_ACCESS:
#             form = crud.form.get(db, product.connected_form_id)
#
#             crud.user.remove_purchased_form(db, user, form)


def enot_payment_url(
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    db: Annotated[Session, Depends(deps.get_db)],
    response: Response,
    value: int,
    promo: str = None,
) -> InvoiceCreateResponse:
    promo_obj: crud.promo.model | None = None

    if promo and (
        not (promo_obj := crud.promo.get_by_name(db, promo))
        or promo_obj.valid_to < datetime.now()
    ):
        raise HTTPException(400, f"No promo `{promo}` was found")

    amount = value

    # for product_id in products:
    #     product = crud.product.get(db, product_id)
    #
    #     if not product:
    #         raise HTTPException(404, f"Product with id {product_id} doesn't exists.")
    #
    #     user = crud.user.get_by_discord_id(db, guild_member.user.id)
    #
    #     if (
    #         ProductOperation(product.operation) == ProductOperation.TICKET_ACCESS
    #         and product.connected_form in user.purchased_forms
    #     ):
    #         raise HTTPException(400, f"Product with id {product_id} already purchased.")
    #
    #     amount += product.price

    if promo_obj:
        amount -= (amount / 100) * promo_obj.percent

    amount = int(amount)

    headers = {"x-api-key": config.ENOT_API_KEY}

    data = {
        "amount": amount,
        "order_id": str(uuid.uuid4()),
        "shop_id": config.SHOP_ID,
        "comment": (
            f"Пополнение баланса | {guild_member.user.id} | {value} mn | {promo if promo else '-'}"
        ),
        "custom_fields": {
            "value": value,
            "guild_member_id": guild_member.user.id,
            "promo": promo,
        },
    }

    enot_resp: HTTPXResponse

    try:
        enot_resp = post(
            url="https://api.enot.io/invoice/create", headers=headers, json=data
        )
    except HTTPError:
        raise HTTPException(500)

    resp_data = payment.enot.InvoiceCreateResponse.model_validate(enot_resp.json())
    response.status_code = enot_resp.status_code

    return resp_data


@router.get("/balance")
def get_balance(
    db: Annotated[Session, Depends(deps.get_db)],
    discord_user: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
) -> int:
    return crud.user.get_by_discord_id(db, discord_user.user.id).money


@router.post("/purchase")
def purchase_product(
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    db: Annotated[Session, Depends(deps.get_db)],
    product_id: int,
    username: str | None = None,
):
    user = crud.user.get_by_discord_id(db, guild_member.user.id)

    if not product_id:
        raise HTTPException(400, "Missing parameters.")

    product = crud.product.get(db, product_id)

    if not product:
        raise HTTPException(404, "Product not found.")

    if product.price > user.money:
        raise HTTPException(400, "Not enough money to purchase.")

    process_product_purchase(db, user, product, username)

    crud.user.update(db, user, UserUpdate(money=user.money - product.price))


@router.post("/payment-url")
def create_payment_url(
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    db: Annotated[Session, Depends(deps.get_db)],
    response: Response,
    value: int,
    promo: str = None,
    provider: PaymentProvider = PaymentProvider.ENOT,
) -> InvoiceCreateResponse:
    match provider:
        case PaymentProvider.ENOT:
            return enot_payment_url(guild_member, db, response, value, promo)


def enot_check_signature(hook_body: dict, header_signature: str):
    sorted_hook_json = dumps(hook_body, sort_keys=True, separators=(", ", ": "))

    secret_key = config.ENOT_API_SIGNATURE.encode("utf-8")

    calc_sign = hmac.new(
        secret_key, msg=sorted_hook_json.encode("utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(header_signature, calc_sign)


@router.post("/enot-webhook")
def enot_payment_webhook(
    data: payment.SuccessfulPayment | payment.UnsuccessfulPayment | payment.Refund,
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    if enot_check_signature(
        data.model_dump(mode="json"), request.headers.get("x-api-sha256-signature")
    ):
        raise HTTPException(401, "Wrong x-api-sha256-signature.")

    value = data.custom_fields.get("value")

    if not value:
        raise HTTPException(400, "Missing value field.")

    guild_member_id = data.custom_fields.get("guild_member_id")
    user = crud.user.get_by_discord_id(db, guild_member_id)

    if not user:
        raise HTTPException(404, "User not found.")

    match type(data):
        case payment.SuccessfulPayment:
            process_value_purchase(db, user, value)
        case payment.Refund:
            raise HTTPException(400, "Refund is not available.")
