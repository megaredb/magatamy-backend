from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from routes.api import deps
from routes.api.v1.discord import auth_middleware
from routes.api.v1.discord.auth import only_admin

router = APIRouter(prefix="/forms", tags=["forms"])


@router.get("/", response_model=List[schemas.ticket.form.Form])
async def read_forms(
    db: Annotated[Session, Depends(deps.get_db)],
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    skip: int = 0,
    limit: int = 100,
):
    """
    Read all forms.
    """

    forms = crud.form.get_multi(db=db, skip=skip, limit=limit)

    resp = []

    for form in forms:
        form_schema: schemas.ticket.form.Form = schemas.ticket.form.Form.model_validate(
            form
        )

        if form.purchasable:
            form_schema.has_access = False

            if (
                form
                in crud.user.get_by_discord_id(db, guild_member.user.id).purchased_forms
            ):
                form_schema.has_access = True

        resp.append(form_schema)

    return resp


@router.get("/{form_id}", response_model=schemas.ticket.form.Form)
async def read_form(
    db: Annotated[Session, Depends(deps.get_db)],
    guild_member: Annotated[schemas.DiscordGuildMember, Depends(auth_middleware)],
    form_id: int,
):
    """
    Read form.
    """

    form = crud.form.get(db=db, _id=form_id)

    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    resp: schemas.ticket.form.Form = schemas.ticket.form.Form.model_validate(form)

    if form.purchasable:
        resp.has_access = False

        if (
            form
            in crud.user.get_by_discord_id(db, guild_member.user.id).purchased_forms
        ):
            resp.has_access = True

    return resp


@router.post("/", response_model=schemas.ticket.form.Form)
async def create_form(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    form_in: schemas.ticket.form.FormCreate,
):
    """
    Create new form.
    """

    return crud.form.create(db=db, obj_in=form_in)


@router.patch("/{form_id}", response_model=schemas.ticket.form.Form)
async def update_form(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    form_id: int,
    form_in: schemas.ticket.form.FormUpdate,
):
    """
    Update form.
    """

    form = crud.form.get(db=db, _id=form_id)

    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    return crud.form.update(db=db, db_obj=form, obj_in=form_in)


@router.delete("/{form_id}", response_model=schemas.ticket.form.Form)
async def remove_form(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    form_id: int,
):
    """
    Remove form.
    """

    return crud.form.remove(db=db, _id=form_id)
