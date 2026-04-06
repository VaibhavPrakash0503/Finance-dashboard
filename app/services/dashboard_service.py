from sqlalchemy.orm import Session
from app.models import FinancialRecord, User, UserRole, RecordType
from datetime import date
from typing import Optional


class DashboardService:
    @staticmethod
    def get_summary(
        db: Session,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Get overall financial summary
        - Admins see all records
        - Viewers/Analysts see only their own records
        """
        query = db.query(FinancialRecord)

        # Apply role-based filtering
        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        # Apply date range filters
        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)
        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)

        # Get all records (we'll calculate in Python for simplicity)
        records = query.all()

        total_income = sum(r.amount for r in records if r.type == RecordType.INCOME)
        total_expenses = sum(r.amount for r in records if r.type == RecordType.EXPENSE)
        net_balance = total_income - total_expenses
        record_count = len(records)

        return {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "net_balance": round(net_balance, 2),
            "record_count": record_count,
        }

    @staticmethod
    def get_category_totals(
        db: Session,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Get category-wise breakdown of income and expenses
        - Admins see all records
        - Viewers/Analysts see only their own records
        """
        query = db.query(FinancialRecord)

        # Apply role-based filtering
        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        # Apply date range filters
        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)
        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)

        records = query.all()

        # Group by category and type
        income_by_category = {}
        expense_by_category = {}

        for record in records:
            if record.type == RecordType.INCOME:
                income_by_category[record.category] = (
                    income_by_category.get(record.category, 0) + record.amount
                )
            elif record.type == RecordType.EXPENSE:
                expense_by_category[record.category] = (
                    expense_by_category.get(record.category, 0) + record.amount
                )

        # Round values to 2 decimal places
        income_by_category = {k: round(v, 2) for k, v in income_by_category.items()}
        expense_by_category = {k: round(v, 2) for k, v in expense_by_category.items()}

        return {
            "income_by_category": income_by_category,
            "expense_by_category": expense_by_category,
        }

    @staticmethod
    def get_recent_activity(
        db: Session, user: User, limit: int = 10
    ) -> list[FinancialRecord]:
        """
        Get recent financial records
        - Admins see all records
        - Viewers/Analysts see only their own records
        """
        query = db.query(FinancialRecord)

        # Apply role-based filtering
        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        # Order by date descending and limit
        records = query.order_by(FinancialRecord.date.desc()).limit(limit).all()

        return records

    @staticmethod
    def get_monthly_trends(
        db: Session,
        user: User,
        months: int = 6,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[dict]:
        """
        Get monthly income/expense trends
        - Admins see all records
        - Viewers/Analysts see only their own records
        - Returns last N months or custom date range
        """
        query = db.query(FinancialRecord)

        # Apply role-based filtering
        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        # Apply date range filters
        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)
        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)

        records = query.all()

        # Group by year-month
        monthly_data = {}
        for record in records:
            period = record.date.strftime("%Y-%m")  # e.g., "2026-04"

            if period not in monthly_data:
                monthly_data[period] = {"income": 0.0, "expenses": 0.0}

            if record.type == RecordType.INCOME:
                monthly_data[period]["income"] += record.amount
            elif record.type == RecordType.EXPENSE:
                monthly_data[period]["expenses"] += record.amount

        # Convert to list and sort by period
        trends = []
        for period in sorted(monthly_data.keys(), reverse=True)[:months]:
            data = monthly_data[period]
            trends.append(
                {
                    "period": period,
                    "income": round(data["income"], 2),
                    "expenses": round(data["expenses"], 2),
                    "net": round(data["income"] - data["expenses"], 2),
                }
            )

        # Reverse to get chronological order (oldest to newest)
        trends.reverse()

        return trends

    @staticmethod
    def get_weekly_trends(
        db: Session,
        user: User,
        weeks: int = 4,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[dict]:
        """
        Get weekly income/expense trends
        - Admins see all records
        - Viewers/Analysts see only their own records
        - Returns last N weeks or custom date range
        """
        query = db.query(FinancialRecord)

        # Apply role-based filtering
        if user.role != UserRole.Admin:
            query = query.filter(FinancialRecord.user_id == user.id)

        # Apply date range filters
        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)
        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)

        records = query.all()

        # Group by ISO week (year-week format)
        weekly_data = {}
        for record in records:
            # ISO week format: "2026-W14"
            iso_calendar = record.date.isocalendar()
            period = f"{iso_calendar[0]}-W{iso_calendar[1]:02d}"

            if period not in weekly_data:
                weekly_data[period] = {"income": 0.0, "expenses": 0.0}

            if record.type == RecordType.INCOME:
                weekly_data[period]["income"] += record.amount
            elif record.type == RecordType.EXPENSE:
                weekly_data[period]["expenses"] += record.amount

        # Convert to list and sort by period
        trends = []
        for period in sorted(weekly_data.keys(), reverse=True)[:weeks]:
            data = weekly_data[period]
            trends.append(
                {
                    "period": period,
                    "income": round(data["income"], 2),
                    "expenses": round(data["expenses"], 2),
                    "net": round(data["income"] - data["expenses"], 2),
                }
            )

        # Reverse to get chronological order (oldest to newest)
        trends.reverse()

        return trends
