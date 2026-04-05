from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import verify_password, create_access_token
from fastapi import HTTPException, status


class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if user.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        access_token = create_access_token(data={"sub": user.email})

        return access_token
