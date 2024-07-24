from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from models import Ticket
from routes.api import deps
from routes.api.v1.discord.auth import auth_middleware, only_moderator
from routes.api.v1.ticket import form, question
from schemas import TicketCreate, TicketUpdate
from utils.discord.user import send_message, send_ticket_update, send_roles_update
from utils.minecraft import ServerEnum
from utils.ticket import TicketStatus

router = APIRouter(prefix="/tickets", tags=["tickets"])
router.include_router(form.router)
router.include_router(question.router)


@router.get("/my", response_model=List[schemas.ticket.Ticket])
async def read_own_tickets(
    db: Annotated[Session, Depends(deps.get_db)],
    discord_user: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
):
    """
    Read own tickets.
    """

    user = crud.user.get_by_discord_id(db, discord_user.user.id)

    tickets = crud.ticket.get_multi_by_author(db=db, author_id=user.discord_id)

    tickets_schemas = []

    for ticket in tickets:
        ticket_schema = schemas.ticket.Ticket.model_validate(ticket)

        tickets_schemas.append(ticket_schema)

    return tickets_schemas


@router.get("/", response_model=List[schemas.ticket.Ticket])
async def read_tickets(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_moderator)],
    ticket_status: TicketStatus = TicketStatus.OPEN,
    skip: int = 0,
    limit: int = 100,
):
    """
    Read tickets.
    """

    if limit > 1000:
        limit = 1000

    tickets = crud.ticket.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        custom_expr=(Ticket.status == ticket_status.value),
    )

    tickets_schemas = []

    for ticket in tickets:
        ticket_schema = schemas.ticket.Ticket.model_validate(ticket)

        tickets_schemas.append(ticket_schema)

    return tickets_schemas


@router.patch("/{ticket_id}", response_model=schemas.ticket.Ticket)
async def update_ticket(
    db: Annotated[Session, Depends(deps.get_db)],
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(only_moderator)],
    ticket_id: int,
    ticket_in: TicketUpdate,
):
    ticket = crud.ticket.get(db=db, _id=ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status != TicketStatus.OPEN and not guild_member.is_admin:
        raise HTTPException(
            status_code=401, detail="Moderators can't change already processed tickets."
        )

    await send_ticket_update(ticket, ticket_in, guild_member)

    if ticket_in.status == TicketStatus.ACCEPTED:
        await send_roles_update(ticket.author_id, ServerEnum(ticket.form.extra_id))

    return crud.form.update(db=db, db_obj=ticket, obj_in=ticket_in)


@router.post("/", response_model=schemas.ticket.Ticket)
async def create_ticket(
    *,
    db: Annotated[Session, Depends(deps.get_db)],
    ticket_in: schemas.ticket.TicketCreateIn,
    discord_user: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
):
    """
    Create new ticket.
    """

    user = crud.user.get_by_discord_id(db, discord_user.user.id)

    if not crud.form.get(db, ticket_in.form_id):
        raise HTTPException(400, "Requested form is not found.")

    last_ticket = crud.ticket.get_multi_by_author(db=db, author_id=user.discord_id)

    if last_ticket:
        last_ticket = last_ticket[-1]

    if last_ticket and TicketStatus(last_ticket.status) == TicketStatus.OPEN:
        raise HTTPException(400, "You already have an opened ticket.")

    form_in = crud.form.get(db, ticket_in.form_id)
    has_access = not form_in.purchasable

    if not has_access:
        for purchased_form in crud.user.get_by_discord_id(
            db, discord_user.user.id
        ).purchased_forms:
            if ticket_in.form_id == purchased_form.id:
                has_access = True

                break

    if not has_access:
        raise HTTPException(
            400, "This ticket is available only for customers who purchased it."
        )

    ticket_create = TicketCreate(**ticket_in.model_dump())

    ticket = crud.ticket.create_with_author(
        db=db, obj_in=ticket_create, author_id=user.discord_id
    )

    for answer_in in ticket_in.answers:
        req_question = crud.question.get(db=db, _id=answer_in.question_id)

        if not req_question:
            raise HTTPException(
                400, f"Requested question {answer_in.question_id} is not found."
            )

        crud.answer.create_with_ticket(db=db, obj_in=answer_in, ticket_id=ticket.id)

    db.refresh(ticket)

    ticket_schema = schemas.ticket.Ticket.model_validate(ticket)

    return ticket_schema
