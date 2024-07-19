import hashlib
import hmac
import uuid
from datetime import datetime
from json import dumps
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from httpx import post, HTTPError, Response as HTTPXResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

import crud
import schemas
from models import Product, User
from routes.api import deps
from routes.api.v1.discord import auth_middleware
from schemas import payment
from schemas.payment import PaymentProvider
from schemas.payment.enot import InvoiceCreateResponse
from utils import config
from utils.product import ProductOperation

router = APIRouter(prefix="/payment", tags=["payment"])


def process_successful_payment(db: Session, user: User, product: Product):
    match ProductOperation(product.operation):
        case ProductOperation.TICKET_ACCESS:
            form = crud.form.get(db, product.connected_form_id)

            crud.user.add_purchased_form(db, user, form)


def process_refund(db: Session, user: User, product: Product):
    match ProductOperation(product.operation):
        case ProductOperation.TICKET_ACCESS:
            form = crud.form.get(db, product.connected_form_id)

            crud.user.remove_purchased_form(db, user, form)


def _enot_payment_url(
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    db: Annotated[Session, Depends(deps.get_db)],
    products: List[int],
    response: Response,
    promo: str = None,
) -> InvoiceCreateResponse:
    products = list(set(products))

    if not products:
        raise HTTPException(400, "No products passed.")

    promo_obj: crud.promo.model | None = None

    if promo and (
        not (promo_obj := crud.promo.get_by_name(db, promo))
        or promo_obj.valid_to < datetime.now()
    ):
        raise HTTPException(400, "No promo was found")

    amount = 0

    for product_id in products:
        product = crud.product.get(db, product_id)

        if not product:
            raise HTTPException(404, f"Product with id {product_id} doesn't exists.")

        user = crud.user.get_by_discord_id(db, guild_member.user.id)

        if (
            ProductOperation(product.operation) == ProductOperation.TICKET_ACCESS
            and product.connected_form in user.purchased_forms
        ):
            raise HTTPException(400, f"Product with id {product_id} already purchased.")

        amount += product.price

    if promo_obj:
        amount -= (amount / 100) * promo_obj.percent

    amount = int(amount)

    headers = {"x-api-key": config.ENOT_API_KEY}

    data = {
        "amount": amount,
        "order_id": str(uuid.uuid4()),
        "shop_id": config.SHOP_ID,
        "comment": (
            f"Оплата товаров | {guild_member.user.id} | {products} | {promo if promo else '-'}"
        ),
        "custom_fields": {
            "products": products,
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


@router.post("/payment-url")
def create_payment_url(
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    db: Annotated[Session, Depends(deps.get_db)],
    products: List[int],
    response: Response,
    promo: str = None,
    provider: PaymentProvider = PaymentProvider.ENOT,
) -> InvoiceCreateResponse:
    match provider:
        case PaymentProvider.ENOT:
            return _enot_payment_url(guild_member, db, products, response, promo)
        case PaymentProvider.VOLET:
            raise NotImplementedError


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

    products = data.custom_fields.get("products")
    guild_member_id = data.custom_fields.get("guild_member_id")

    for product_id in products:
        if not product_id or not guild_member_id:
            raise HTTPException(400, "Missing parameters.")

        product = crud.product.get(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found.")

        user = crud.user.get_by_discord_id(db, guild_member_id)

        if not user:
            raise HTTPException(404, "User not found.")

        match type(data):
            case payment.SuccessfulPayment:
                process_successful_payment(db, user, product)
            case payment.Refund:
                process_refund(db, user, product)
