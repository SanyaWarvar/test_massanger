from fastapi import APIRouter, Depends, HTTPException

from src.auth.auth_handler import sign_jwt
from src.auth.utils import pwd_contex
from src.auth.schemes import UserScheme
from src.db_manager import DBManager
from src.database import get_async_session
from src.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
async def register(user: UserScheme, session=Depends(get_async_session)):
    try:
        await DBManager.create_user(
            session,
            User(
                username=user.username,
                hashed_password=pwd_contex.hash(user.password)
            )
        )
    except ValueError:
        raise HTTPException(400, "Username is exists!")

    token = sign_jwt(user.username)
    response = {
        "status_code": 201,
        "access_token": token
    }
    return response


@router.post("/login")
async def login(user: UserScheme, session=Depends(get_async_session)):

    res = await DBManager.get_user_by_username(session, user.username)
    print(res.hashed_password , pwd_contex.hash(user.password))
    if not res :
        raise HTTPException(400, "Incorrect data!")

    token = sign_jwt(user.username)
    response = {
        "status_code": 201,
        "access_token": token
    }
    return response
