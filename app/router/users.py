from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.dependencies import get_current_active_user, require_role
from app.models import UserRole, User

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Create a new user (Admin only).

    Provide username, email, password, and role to create a new user.
    Valid roles are: admin, manager, viewer.
    """
    return UserService.create_user(user_data=user_data, db=db)


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Get all users (Admin and Manager only).

    Retrieve a list of all registered users in the system.
    """
    return UserService.get_all_users(db=db)


@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile.

    Retrieve the profile information of the currently authenticated user.
    """
    return current_user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Delete a user by ID (Admin only).

    Provide the user ID to delete the corresponding user from the system.
    """
    UserService.delete_user(user_id=user_id, db=db)
