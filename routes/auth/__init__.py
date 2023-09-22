from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from starlette import status

from utils import auth
from utils.auth import oauth2_scheme, create_access_token, SECRET_KEY, ALGORITHM

api_router = APIRouter()


async def check_user_validity(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != auth.ADMIN_LOGIN:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


@api_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != auth.ADMIN_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    if not auth.verify_password(form_data.password, auth.ADMIN_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token({
            "sub": form_data.username,
        }),
        "token_type": "bearer",
    }
