from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from db_models import User
from .operations import create_default_user_dataset_and_model
from .schemas import Token, UserRegisterSchema
from .utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, pwd_context


router = APIRouter()


@router.post("/register")
def register(user: UserRegisterSchema, db: Annotated[Session, Depends(get_db)]):
    user_obj = User()
    user_obj.login = user.login
    user_obj.password = pwd_context.hash(user.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    create_default_user_dataset_and_model(db, user_obj)


@router.post("/token")
async def login(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.login}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me")
async def current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "login": current_user.login,
    }