from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud
from backend import schemas
from backend.routes.api import deps
from backend.routes.api.v1.discord.auth import only_admin
from backend.utils.ticket import AnswerType

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=schemas.ticket.question.Question)
async def create_question(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    question_in: schemas.ticket.question.QuestionCreate,
):
    """
    Create new question.
    """

    if not crud.form.get(db=db, _id=question_in.form_id):
        raise HTTPException(status_code=404, detail="Requested form is not found.")

    question_in.answer_type = AnswerType(question_in.answer_type)

    return crud.question.create(db=db, obj_in=question_in)


@router.patch("/{question_id}", response_model=schemas.ticket.question.Question)
async def update_question(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    question_id: int,
    question_in: schemas.ticket.question.QuestionUpdate,
):
    """
    Update question.
    """

    question = crud.question.get(db=db, _id=question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Requested question is not found.")

    if not crud.form.get(db=db, _id=question_in.form_id):
        raise HTTPException(status_code=404, detail="Requested form is not found.")

    return crud.form.update(db=db, db_obj=question, obj_in=question_in)


@router.delete("/{question_id}", response_model=schemas.ticket.question.Question)
async def remove_question(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[schemas.DiscordGuildMember, Depends(only_admin)],
    question_id: int,
):
    """
    Remove question.
    """

    return crud.form.remove(db=db, _id=question_id)
