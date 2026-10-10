import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ✅ JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "MY_SECRET_KEY_123")

    # ✅ POSTGRES CONNECTION
    # Example: postgresql://postgres:postgres@localhost:5432/notesapp
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/notesapp",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ ADMIN LOGIN CREDENTIALS
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")

    # ✅ UPLOADS
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max upload size

    # ✅ EMAIL (SMTP) — used to notify users when their note is approved/rejected
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")          # your Gmail address
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # Gmail App Password (not your normal password)
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Notes Sharing Website")
