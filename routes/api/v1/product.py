from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

import crud
import schemas
from routes.api import deps
from routes.api.v1.discord.auth import auth_middleware, only_admin
from schemas import DiscordGuildMember

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.Product])
async def read_products(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
):
    """
    Read all products.
    """
    try:
        discord_user = await auth_middleware(request, db)
    except HTTPException:
        discord_user = None

    if not discord_user:
        return []

    return crud.product.get_multi(db=db, is_admin=discord_user.is_admin())


@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    """
    Create new product.
    """
    return crud.product.create(db=db, obj_in=product_in)


@router.patch("/{product_id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.product.update(db=db, db_obj=product, obj_in=product_in)


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(*, db: Session = Depends(deps.get_db), product_id: int):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    _deps: Annotated[DiscordGuildMember, Depends(only_admin)]
):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.product.remove(db=db, id=product_id)
