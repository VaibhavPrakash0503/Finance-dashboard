from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RecordCreate, RecordResponse, RecordUpdate
from app.services.record_service import RecordService
from app.dependencies import get_current_user, require_role
from app.models import User, UserRole

router = APIRouter()


@router.post("/", response_model=RecordResponse, status_code=201)
def create_record(
    record: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Create Financial record
    - Admins only
    Valid types: INCOME, EXPENSE
    """

    return RecordService.create_record(db, record, current_user.id)


@router.get("/", response_model=list[RecordResponse])
def list_records(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    category: str | None = Query(None, description="Filter by category"),
    record_type: str | None = Query(
        None, description="Filter by type (INCOME or EXPENSE)"
    ),
):
    """
    List financial records

    - **Admins** see all records in the system
    - **Viewers/Analysts** see only their own records

    Optional filters: category, type
    """
    return RecordService.get_records(db, user, skip, limit, category, record_type)


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Update financial record - Admin only

    All fields are optional - only provided fields will be updated.
    """
    return RecordService.update_record(db, record_id, record_data)


@router.delete("/{record_id}", status_code=204)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.Admin)),
):
    """
    Delete financial record - Admin only

    Permanently deletes the record from the system.
    """
    RecordService.delete_record(db, record_id)
    return None
