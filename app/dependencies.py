import jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import DecodeError
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/access-token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY", ""),
            algorithms=[os.environ.get("ALGORITHM", "")],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except DecodeError:
        raise credentials_exception
