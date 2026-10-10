from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # bcrypt hash

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(500), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    uploaded_by = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # pending | approved | rejected
    status = db.Column(db.String(20), default="pending", nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "filename": self.filename,
            "filepath": self.filepath,
            "uploadedBy": self.uploaded_by,
            "date": self.date.isoformat() if self.date else None,
            "status": self.status,
        }
