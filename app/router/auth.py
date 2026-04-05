from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.database import get_db
from app.schemas import TokenResponse, LoginRequest

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT access token.

    Provide your email and password to receive a JWT token.
    The token expires in 30 minutes.
    """
    access_token = AuthService.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    return {"access_token": access_token, "token_type": "bearer"}
