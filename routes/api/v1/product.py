from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from routes.api import deps
from routes.auth import check_user_validity

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(deps.get_db)):
    """
    Read all products.
    """
    return crud.product.get_multi(db=db)


@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    _deps: Annotated[str, Depends(check_user_validity)]
):
    """
    Create new product.
    """
    return crud.product.create(db=db, obj_in=product_in)


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    _deps: Annotated[str, Depends(check_user_validity)]
):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.product.update(db=db, db_obj=product, obj_in=product_in)


@router.get("/{id}", response_model=schemas.Product)
def read_product(*, db: Session = Depends(deps.get_db), product_id: int):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    _deps: Annotated[str, Depends(check_user_validity)]
):
    product = crud.product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.product.remove(db=db, id=product_id)
