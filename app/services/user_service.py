from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.schemas import UserCreate
from app.utils.security import hash_password
from fastapi import HTTPException, status


class UserService:
    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        """Create new user."""

        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        try:
            role_enum = UserRole(user_data.role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Valid roles are: {[role.value for role in UserRole]}",
            )
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=role_enum,
            is_active=True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_all_users(db: Session):
        """Get all users."""
        return db.query(User).all()

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        """Get user by email."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
