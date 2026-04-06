from fastapi import FastAPI
from app.database import init_db
from app.utils.seed import seed_admin
from app.router import auth, users, records, dashboard

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend API for finance dashboard with role-based access control",
    version="1.0.0",
)


# Create tables on startup
@app.on_event("startup")
def startup_event():
    print("🚀 Starting Finance Dashboard API...")
    init_db()
    print("📊 Database tables initialized")
    seed_admin()
    print("✅ Startup complete!")


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(records.router, prefix="/api/records", tags=["Financial Records"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
