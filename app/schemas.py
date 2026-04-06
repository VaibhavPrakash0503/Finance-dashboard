from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
from typing import ClassVar


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=8, examples=["SecurePass123!"])
    role: str = Field(..., examples=["Analyst"], description="Must be one of: Viewer, Analyst, Admin")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive", examples=[1500.00])
    type: str = Field(..., examples=["INCOME"], description="Must be INCOME or EXPENSE")
    description: str | None = Field(None, max_length=500, examples=["Monthly salary payment"])
    category: str = Field(..., examples=["Salary"], description="Must be from predefined list")
    date: datetime = Field(..., examples=["2026-04-01T00:00:00"])
    user_id: int | None = Field(
        None, examples=[2], description="Optional - Admin can specify user, otherwise defaults to creator"
    )

    # Predefined categories
    INCOME_CATEGORIES: ClassVar[list[str]] = [
        "Salary",
        "Freelance",
        "Investment",
        "Gift",
        "Other Income",
    ]
    EXPENSE_CATEGORIES: ClassVar[list[str]] = [
        "Rent",
        "Food",
        "Transport",
        "Entertainment",
        "Healthcare",
        "Shopping",
        "Utilities",
        "Education",
        "Insurance",
        "Other Expense",
    ]
    ALL_CATEGORIES: ClassVar[list[str]] = INCOME_CATEGORIES + EXPENSE_CATEGORIES

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        if v > 1_000_000_000:
            raise ValueError("Amount cannot exceed 1 billion")
        # Round to 2 decimal places
        return round(v, 2)

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        today = datetime.now()
        # Convert datetime to date for comparison
        record_date = v.date() if isinstance(v, datetime) else v

        # No future dates
        if record_date > today.date():
            raise ValueError("Date cannot be in the future")

        # Not too old (10 years)
        ten_years_ago = today.replace(year=today.year - 10).date()
        if record_date < ten_years_ago:
            raise ValueError("Date cannot be more than 10 years in the past")

        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        if v not in cls.ALL_CATEGORIES:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(cls.ALL_CATEGORIES)}"
            )
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Description cannot be empty or whitespace only")
        return v


class RecordUpdate(BaseModel):
    amount: float | None = Field(None, gt=0, description="Amount must be positive")
    type: str | None = None
    description: str | None = Field(None, max_length=500)
    category: str | None = None
    date: datetime | None = None
    user_id: int | None = None  # Optional - Admin can reassign record to different user

    # Predefined categories (same as RecordCreate)
    INCOME_CATEGORIES: ClassVar[list[str]] = [
        "Salary",
        "Freelance",
        "Investment",
        "Gift",
        "Other Income",
    ]
    EXPENSE_CATEGORIES: ClassVar[list[str]] = [
        "Rent",
        "Food",
        "Transport",
        "Entertainment",
        "Healthcare",
        "Shopping",
        "Utilities",
        "Education",
        "Insurance",
        "Other Expense",
    ]
    ALL_CATEGORIES: ClassVar[list[str]] = INCOME_CATEGORIES + EXPENSE_CATEGORIES

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Amount must be greater than 0")
            if v > 1_000_000_000:
                raise ValueError("Amount cannot exceed 1 billion")
            # Round to 2 decimal places
            return round(v, 2)
        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            today = datetime.now()
            # Convert datetime to date for comparison
            record_date = v.date() if isinstance(v, datetime) else v

            # No future dates
            if record_date > today.date():
                raise ValueError("Date cannot be in the future")

            # Not too old (10 years)
            ten_years_ago = today.replace(year=today.year - 10).date()
            if record_date < ten_years_ago:
                raise ValueError("Date cannot be more than 10 years in the past")

        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        if v is not None and v not in cls.ALL_CATEGORIES:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(cls.ALL_CATEGORIES)}"
            )
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Description cannot be empty or whitespace only")
        return v


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    description: str | None = None
    date: datetime
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
        use_enum_values = True


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["admin@finance.com"])
    password: str = Field(..., examples=["admin123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    role: str


# Dashboard Schemas
class SummaryResponse(BaseModel):
    """Overall financial summary"""

    total_income: float
    total_expenses: float
    net_balance: float
    record_count: int


class CategoryTotal(BaseModel):
    """Category-wise breakdown"""

    category: str
    total: float


class CategoryTotalsResponse(BaseModel):
    """Income and expense totals by category"""

    income_by_category: dict[str, float]
    expense_by_category: dict[str, float]


class TrendDataPoint(BaseModel):
    """Single data point for trends"""

    period: str  # e.g., "2026-04" for monthly, "2026-W14" for weekly
    income: float
    expenses: float
    net: float


class TrendsResponse(BaseModel):
    """Trends over time"""

    trends: list[TrendDataPoint]


class RecentActivityResponse(BaseModel):
    """Recent financial records"""

    recent_records: list[RecordResponse]
