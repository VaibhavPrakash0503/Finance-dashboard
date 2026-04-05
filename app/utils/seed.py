from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, UserRole
from app.utils.security import hash_password


def seed_admin():
    db = SessionLocal()
    admin_email = "admin@finance.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()

    try:
        if not existing_admin:
            admin_user = User(
                username="admin",
                email=admin_email,
                password_hash=hash_password("admin123"),
                role=UserRole.Admin,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created successfully!")
            print(f"   Email: {admin_email}")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Role: Admin")
        else:
            print("✅ Admin user already exists.")
    except Exception as e:
        print(f"❌ Error seeding admin user: {e}")
        db.rollback()
    finally:
        db.close()
