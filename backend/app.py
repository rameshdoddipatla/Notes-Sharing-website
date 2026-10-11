import os
import time

import bcrypt
import jwt
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import Config
from email_utils import send_status_email
from models import Note, User, db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

with app.app_context():
    db.create_all()


# ✅ SERVE UPLOADED FILES  (equivalent of app.use("/uploads", express.static("uploads")))
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


# ✅ USER REGISTER
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    try:
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"success": False, "message": "User already exists!"})

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True, "message": "Registered Successfully"})
    except Exception as err:
        print("REGISTER ERROR:", err)
        db.session.rollback()
        return jsonify({"success": False, "message": "Registration failed"})


# ✅ USER LOGIN
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found!"})

    match = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    if not match:
        return jsonify({"success": False, "message": "Invalid password!"})

    token = jwt.encode({"email": email}, Config.JWT_SECRET, algorithm="HS256")

    return jsonify({"success": True, "message": "Login Successful", "token": token})


# ✅ ADMIN LOGIN
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if email == Config.ADMIN_EMAIL and password == Config.ADMIN_PASSWORD:
        token = jwt.encode(
            {"role": "admin", "exp": int(time.time()) + 24 * 60 * 60},
            Config.JWT_SECRET,
            algorithm="HS256",
        )
        return jsonify(
            {"success": True, "message": "Admin Login Successful", "token": token}
        )

    return jsonify({"success": False, "message": "Invalid Admin Credentials"})


# ✅ ✅ ✅ POINT 2 — UPLOAD NOTE (STATUS = "pending")
@app.route("/api/upload", methods=["POST"])
def upload_note():
    try:
        title = request.form.get("title")
        uploaded_by = request.form.get("uploadedBy")
        file = request.files.get("file")

        if not file or file.filename == "":
            return jsonify({"success": False, "message": "No file selected"})

        filename = f"{int(time.time() * 1000)}-{secure_filename(file.filename)}"
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        note = Note(
            title=title,
            filename=filename,
            filepath=f"/uploads/{filename}",
            uploaded_by=uploaded_by,
            status="pending",
        )
        db.session.add(note)
        db.session.commit()

        return jsonify(
            {"success": True, "message": "File Uploaded! Waiting for Admin Approval."}
        )
    except Exception as error:
        print("UPLOAD ERROR:", error)
        db.session.rollback()
        return jsonify({"success": False, "message": "Upload Failed"})


# ✅ ✅ ✅ POINT 3 — ADMIN: GET ALL PENDING NOTES
@app.route("/api/admin/pending", methods=["GET"])
def get_pending_notes():
    try:
        notes = Note.query.filter_by(status="pending").all()
        return jsonify([n.to_dict() for n in notes])
    except Exception as error:
        print("ADMIN PENDING ERROR:", error)
        return jsonify([])


# ✅ ADMIN APPROVE NOTE
@app.route("/api/admin/approve/<int:note_id>", methods=["PUT"])
def approve_note(note_id):
    try:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({"success": False, "message": "Note not found"})
        note.status = "approved"
        db.session.commit()

        send_status_email(note.uploaded_by, note.title, "approved")

        return jsonify({"success": True, "message": "Note Approved"})
    except Exception as err:
        print("APPROVE ERROR:", err)
        db.session.rollback()
        return jsonify({"success": False, "message": "Approve Failed"})


# ✅ ADMIN REJECT NOTE
@app.route("/api/admin/reject/<int:note_id>", methods=["PUT"])
def reject_note(note_id):
    try:
        note = Note.query.get(note_id)
        if not note:
            return jsonify({"success": False, "message": "Note not found"})
        note.status = "rejected"
        db.session.commit()

        send_status_email(note.uploaded_by, note.title, "rejected")

        return jsonify({"success": True, "message": "Note Rejected"})
    except Exception as err:
        print("REJECT ERROR:", err)
        db.session.rollback()
        return jsonify({"success": False, "message": "Reject Failed"})


# ✅ GET ONLY APPROVED NOTES (FOR STUDENTS)
@app.route("/api/notes", methods=["GET"])
def get_approved_notes():
    notes = Note.query.filter_by(status="approved").order_by(Note.date.desc()).all()
    return jsonify([n.to_dict() for n in notes])


# HOME PAGE
@app.route("/")
def home():
    frontend_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "frontend")
    )
    return send_from_directory(frontend_folder, "index.html")
    
# ✅ START SERVER
if __name__ == "__main__":
    app.run(port=5000, debug=True)
