from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from routes.api import deps
from routes.api.v1.discord.auth import only_admin
from schemas import DiscordGuildMember

router = APIRouter(prefix="/promos", tags=["promo"])


@router.get("/", response_model=List[schemas.Promo])
async def read_promos(
    db: Annotated[Session, Depends(deps.get_db)],
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)],
):
    """
    Read all promos.
    """

    return crud.promo.get_multi(db=db)


@router.post("/", response_model=schemas.Promo)
def create_promo(
    *,
    db: Session = Depends(deps.get_db),
    promo_in: schemas.PromoCreate,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    """
    Create new promo.
    """
    return crud.promo.create(db=db, obj_in=promo_in)


@router.patch("/{promo_id}", response_model=schemas.Promo)
def update_promo(
    *,
    db: Session = Depends(deps.get_db),
    promo_id: int,
    promo_in: schemas.PromoUpdate,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    promo = crud.product.get(db, promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return crud.promo.update(db=db, db_obj=promo, obj_in=promo_in)


@router.get("/{promo_id}", response_model=schemas.Promo)
def read_promo(*, db: Session = Depends(deps.get_db), promo_id: int):
    promo = crud.promo.get(db, promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return promo


@router.delete("/{promo_id}", response_model=schemas.Promo)
def delete_promo(
    *,
    db: Session = Depends(deps.get_db),
    promo_id: int,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    promo = crud.promo.get(db, promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return crud.promo.remove(db=db, _id=promo_id)
