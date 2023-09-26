from api.auth.schemas import Token, TokenData
from core.auth.services import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


async def get_access_token(username: str, password: str) -> Token:
    """Get access token"""

    if username != "user" or password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="bearer")
