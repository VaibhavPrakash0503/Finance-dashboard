from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    SummaryResponse,
    CategoryTotalsResponse,
    TrendsResponse,
    RecentActivityResponse,
)
from app.services.dashboard_service import DashboardService
from app.dependencies import get_current_user, require_role, require_roles
from app.models import User, UserRole
from datetime import date
from typing import Optional

router = APIRouter()


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.Analyst, UserRole.Admin])),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
):
    """
    Get overall financial summary

    Returns:
    - Total income
    - Total expenses
    - Net balance (income - expenses)
    - Total record count

    **Access:** Analyst and Admin only
    - Admins see all records across all users
    - Analysts see only their own records

    Optional date range filtering with start_date and end_date.
    """
    return DashboardService.get_summary(db, current_user, start_date, end_date)


@router.get("/category-totals", response_model=CategoryTotalsResponse)
def get_category_totals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.Analyst, UserRole.Admin])),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
):
    """
    Get category-wise breakdown of income and expenses

    Returns income and expense totals grouped by category.

    **Access:** Analyst and Admin only
    - Admins see all records across all users
    - Analysts see only their own records

    Optional date range filtering with start_date and end_date.
    """
    return DashboardService.get_category_totals(db, current_user, start_date, end_date)


@router.get("/recent-activity", response_model=RecentActivityResponse)
def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.Analyst, UserRole.Admin])),
    limit: int = Query(10, ge=1, le=100, description="Number of recent records to return"),
):
    """
    Get recent financial records

    Returns the most recent financial records ordered by date.

    **Access:** Analyst and Admin only
    - Admins see all records across all users
    - Analysts see only their own records

    Limit parameter controls how many records to return (1-100, default: 10).
    """
    records = DashboardService.get_recent_activity(db, current_user, limit)
    return {"recent_records": records}


@router.get("/trends/monthly", response_model=TrendsResponse)
def get_monthly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.Analyst, UserRole.Admin])),
    months: int = Query(6, ge=1, le=24, description="Number of months to return"),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
):
    """
    Get monthly income/expense trends

    Returns aggregated financial data grouped by month.
    Each trend point includes:
    - Period (YYYY-MM format)
    - Total income
    - Total expenses
    - Net balance

    **Access:** Analyst and Admin only
    - Admins see all records across all users
    - Analysts see only their own records

    Parameters:
    - months: Number of recent months to return (1-24, default: 6)
    - start_date/end_date: Optional date range filtering
    """
    trends = DashboardService.get_monthly_trends(
        db, current_user, months, start_date, end_date
    )
    return {"trends": trends}


@router.get("/trends/weekly", response_model=TrendsResponse)
def get_weekly_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.Analyst, UserRole.Admin])),
    weeks: int = Query(4, ge=1, le=52, description="Number of weeks to return"),
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
):
    """
    Get weekly income/expense trends

    Returns aggregated financial data grouped by ISO week.
    Each trend point includes:
    - Period (YYYY-WNN format, e.g., "2026-W14")
    - Total income
    - Total expenses
    - Net balance

    **Access:** Analyst and Admin only
    - Admins see all records across all users
    - Analysts see only their own records

    Parameters:
    - weeks: Number of recent weeks to return (1-52, default: 4)
    - start_date/end_date: Optional date range filtering
    """
    trends = DashboardService.get_weekly_trends(
        db, current_user, weeks, start_date, end_date
    )
    return {"trends": trends}
