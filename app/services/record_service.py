from sqlalchemy.orm import Session
from app.models import FinancialRecord, User, UserRole, RecordType
from app.schemas import RecordCreate, RecordUpdate
from fastapi import HTTPException, status


class RecordService:
    @staticmethod
    def create_record(
        db: Session, record_data: RecordCreate, creator_id: int
    ) -> FinancialRecord:
        """Create new financial record (Admin only)"""
        try:
            record_enum = RecordType[record_data.type]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type. Must be one of: {[t.name for t in RecordType]}",
            )

        target_user_id = record_data.user_id if record_data.user_id else creator_id

        # Validate that the target user exists
        user_exists = db.query(User).filter(User.id == target_user_id).first()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {target_user_id} not found",
            )

        db_record = FinancialRecord(
            type=record_enum,
            amount=record_data.amount,
            category=record_data.category,
            date=record_data.date,
            description=record_data.description,
            user_id=target_user_id,
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return db_record

    @staticmethod
    def get_records(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 100,
        category: str | None = None,
        record_type: str | None = None,
    ) -> list[FinancialRecord]:
        """
        Get records based on User Role:
        - Admins see all record
        - Viewer/Analysts only see their own records
        """

        query = db.query(FinancialRecord)

        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        if category:
            query = query.filter(FinancialRecord.category == category)

        if record_type:
            try:
                record_enum = RecordType[record_type]
                query = query.filter(FinancialRecord.type == record_enum)
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid type. Must be one of: {[t.name for t in RecordType]}",
                )

        query = query.order_by(FinancialRecord.date.desc())

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_record(
        db: Session, record_id: int, record_data: RecordUpdate
    ) -> FinancialRecord:
        """Update existing record (Admin only)"""

        record = (
            db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found"
            )

        if record_data.type:
            try:
                type_enum = RecordType[record_data.type]
                record.type = type_enum
            except TypeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid type. Must be one of: {[t.name for t in RecordType]}",
                )

            if record_data.user_id is not None:
                user_exists = (
                    db.query(User).filter(User.id == record_data.user_id).first()
                )
                if not user_exists:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {record_data.user_id} not found",
                    )
                record.user_id = record_data.user_id

            if record_data.category is not None:
                record.category = record_data.category

            if record_data.amount is not None:
                record.amount = record_data.amount

            if record_data.date is not None:
                record.date = record_data.date

            if record_data.description is not None:
                record.description = record_data.description

            db.commit()
            db.refresh(record)

            return record

    @staticmethod
    def delete_record(db: Session, record_id: int) -> None:
        """Delete existing record (Admin only)"""

        record = (
            db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found"
            )

        db.delete(record)
        db.commit()
