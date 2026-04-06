# Finance Dashboard API

A backend API for managing financial records with role-based access control, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## 📋 Features

- **User Management**: Create and manage users with different roles
- **Role-Based Access Control (RBAC)**: Three user roles with different permissions
- **Financial Records**: Track income and expenses with categories
- **Dashboard Analytics**: Get summaries, trends, and insights
- **JWT Authentication**: Secure token-based authentication
- **Data Validation**: Comprehensive input validation and error handling

---

## 🔐 User Roles & Permissions

| Role | Records | Dashboard | User Management |
|------|---------|-----------|-----------------|
| **Viewer** | ✅ View own records only | ❌ No access | ❌ No access |
| **Analyst** | ✅ View own records only | ✅ Full access (own data) | ❌ No access |
| **Admin** | ✅ Full CRUD (all records) | ✅ Full access (all data) | ✅ Full access |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd finance-dashborad
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

6. **Access API Documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 👤 Default Admin User

An admin user is automatically created on first startup:

- **Email**: `admin@finance.com`
- **Password**: `admin123`
- **Role**: Admin

⚠️ **Change this password in production!**

---

## 📚 API Endpoints

### 🔐 Authentication

#### POST `/api/auth/login`
Login and get JWT token

**Request:**
```json
{
  "username": "admin@finance.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 👥 User Management

#### POST `/api/users/users` (Admin only)
Create a new user

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "role": "Analyst"
}
```

**Response:**
```json
{
  "id": 2,
  "email": "john@example.com",
  "role": "Analyst",
  "is_active": true,
  "created_at": "2026-04-06T10:00:00"
}
```

#### GET `/api/users/` (Admin only)
Get all users

#### GET `/api/users/me` (All authenticated users)
Get current user information

#### DELETE `/api/users/{user_id}` (Admin only)
Delete a user

---

### 💰 Financial Records

#### POST `/api/records/` (Admin only)
Create a financial record

**Request:**
```json
{
  "amount": 1500.00,
  "type": "INCOME",
  "category": "Salary",
  "date": "2026-04-01T00:00:00",
  "description": "Monthly salary payment",
  "user_id": 2
}
```

**Validation Rules:**
- Amount must be positive (> 0) and ≤ 1 billion
- Date cannot be in the future or older than 10 years
- Category must be from predefined list (see below)
- Description max 500 characters

**Valid Categories:**

**Income:**
- Salary
- Freelance
- Investment
- Gift
- Other Income

**Expense:**
- Rent
- Food
- Transport
- Entertainment
- Healthcare
- Shopping
- Utilities
- Education
- Insurance
- Other Expense

#### GET `/api/records/` (All roles)
List financial records

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Max records to return (default: 100, max: 1000)
- `category`: Filter by category
- `record_type`: Filter by type (INCOME or EXPENSE)

**Behavior:**
- Admins see all records
- Viewers/Analysts see only their own records

#### PUT `/api/records/{record_id}` (Admin only)
Update a financial record

#### DELETE `/api/records/{record_id}` (Admin only)
Delete a financial record

---

### 📊 Dashboard Analytics

All dashboard endpoints require **Analyst or Admin** role.

#### GET `/api/dashboard/summary`
Get overall financial summary

**Query Parameters:**
- `start_date`: Filter start date (optional)
- `end_date`: Filter end date (optional)

**Response:**
```json
{
  "total_income": 50000.00,
  "total_expenses": 30000.00,
  "net_balance": 20000.00,
  "record_count": 150
}
```

#### GET `/api/dashboard/category-totals`
Get category-wise breakdown

**Response:**
```json
{
  "income_by_category": {
    "Salary": 45000.00,
    "Freelance": 5000.00
  },
  "expense_by_category": {
    "Rent": 15000.00,
    "Food": 8000.00,
    "Transport": 3000.00
  }
}
```

#### GET `/api/dashboard/recent-activity`
Get recent financial records

**Query Parameters:**
- `limit`: Number of records (1-100, default: 10)

#### GET `/api/dashboard/trends/monthly`
Get monthly income/expense trends

**Query Parameters:**
- `months`: Number of months to return (1-24, default: 6)
- `start_date`: Filter start date (optional)
- `end_date`: Filter end date (optional)

**Response:**
```json
{
  "trends": [
    {
      "period": "2026-03",
      "income": 4800.00,
      "expenses": 3200.00,
      "net": 1600.00
    },
    {
      "period": "2026-04",
      "income": 5000.00,
      "expenses": 3500.00,
      "net": 1500.00
    }
  ]
}
```

#### GET `/api/dashboard/trends/weekly`
Get weekly income/expense trends

**Query Parameters:**
- `weeks`: Number of weeks to return (1-52, default: 4)

---

## 🔑 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### How to Authenticate:

1. **Login** to get a token:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@finance.com&password=admin123"
```

2. **Use the token** in subsequent requests:
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer <your-token-here>"
```

### Swagger UI Authentication:

1. Click the **"Authorize"** button (lock icon) at the top
2. Enter your email in the **username** field
3. Enter your password
4. Click **"Authorize"**
5. All requests will now include the token automatically

---

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: User role (Viewer, Analyst, Admin)
- `is_active`: Account status
- `created_at`: Registration timestamp

### Financial Records Table
- `id`: Primary key
- `type`: INCOME or EXPENSE
- `amount`: Transaction amount
- `category`: Transaction category
- `date`: Transaction date
- `description`: Optional notes
- `user_id`: Foreign key to users
- `created_at`: Record creation timestamp

---

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Bcrypt**: Password hashing
- **Uvicorn**: ASGI server

---

## 📦 Project Structure

```
finance-dashborad/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── dependencies.py         # Auth dependencies
│   ├── router/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── records.py         # Financial records endpoints
│   │   └── dashboard.py       # Dashboard analytics endpoints
│   ├── services/
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── user_service.py    # User management logic
│   │   ├── record_service.py  # Records management logic
│   │   └── dashboard_service.py # Analytics logic
│   └── utils/
│       ├── security.py        # Password hashing, JWT
│       └── seed.py            # Database seeding
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── finance.db                  # SQLite database (auto-created)
└── README.md                   # This file
```

---

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click **"Authorize"** button
4. Login with admin credentials
5. Test endpoints directly in the UI

### Testing with cURL

**1. Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@finance.com&password=admin123"
```

**2. Create a record:**
```bash
curl -X POST "http://localhost:8000/api/records/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000,
    "type": "INCOME",
    "category": "Salary",
    "date": "2026-04-01T00:00:00"
  }'
```

**3. Get dashboard summary:**
```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer <token>"
```

---

## ⚠️ Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful GET/PUT request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

---

## 🔒 Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- Role-based access control on all endpoints
- Input validation on all requests
- SQL injection prevention via SQLAlchemy ORM

**Production Recommendations:**
- Change default admin password
- Use a stronger SECRET_KEY
- Use PostgreSQL instead of SQLite
- Enable HTTPS/TLS
- Add rate limiting
- Implement refresh tokens

---

## 📝 Development Notes

### Adding New Categories

Edit `app/schemas.py`:
```python
INCOME_CATEGORIES: ClassVar[list[str]] = [
    "Salary",
    "YourNewCategory",  # Add here
    ...
]
```

### Changing Token Expiration

Edit `.env`:
```env
ACCESS_TOKEN_EXPIRE_MINUTES=60  # Change to 60 minutes
```

### Database Migrations

Currently using SQLite with auto-creation. For production:
1. Switch to PostgreSQL
2. Use Alembic for database migrations
3. Add proper migration scripts

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---
