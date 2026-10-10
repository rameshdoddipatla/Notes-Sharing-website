# Notes Sharing Website

**Frontend:** static HTML / CSS / JS
**Backend:** Python (Flask)
**Database:** PostgreSQL

## Project structure

```
notes-sharing-website/
├── frontend/          # static site (unchanged UI, plain HTML/CSS/JS)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   ├── all-notes.html
│   ├── admin-login.html
│   └── admin-pending.html
└── backend/           # Flask API
    ├── app.py          # routes (register/login/upload/admin/notes)
    ├── models.py        # SQLAlchemy models: User, Note
    ├── config.py         # env-driven config
    ├── schema.sql        # optional manual table creation
    ├── requirements.txt
    ├── .env.example
    └── uploads/           # uploaded files are stored here
```

## Backend setup

1. Create a PostgreSQL database:
   ```bash
   createdb notesapp
   ```

2. Install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # edit .env — set JWT_SECRET, DATABASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD
   ```

4. Run the server (tables are created automatically on first run via
   `db.create_all()` — `schema.sql` is provided only if you'd rather create
   them by hand):
   ```bash
   python app.py
   ```
   The API runs at `http://localhost:5000`, matching the URLs the frontend
   already calls.

## Frontend

Just open `frontend/index.html` in a browser, or serve the folder with any
static file server, e.g.:
```bash
cd frontend
python -m http.server 3000

http://localhost:3000
```

## API endpoints (unchanged from the original Node version)

| Method | Endpoint                    | Description                       |
|--------|------------------------------|------------------------------------|
| POST   | `/api/register`              | Register a new user               |
| POST   | `/api/login`                 | User login, returns JWT            |
| POST   | `/api/admin/login`           | Admin login, returns JWT           |
| POST   | `/api/upload`                | Upload a note (status = pending)   |
| GET    | `/api/admin/pending`         | List pending notes (admin)         |
| PUT    | `/api/admin/approve/<id>`    | Approve a note                     |
| PUT    | `/api/admin/reject/<id>`     | Reject a note                      |
| GET    | `/api/notes`                 | List approved notes                |
| GET    | `/uploads/<filename>`        | Serve an uploaded file             |

## Notes on the migration from Node/Mongo → Flask/Postgres

- MongoDB's auto-generated `_id` is replaced by an auto-incrementing
  integer `id` (Postgres `SERIAL`). `admin-pending.html` was updated to use
  `note.id` instead of `note._id` — everything else in the frontend was
  left as-is since the JSON field names (`title`, `uploadedBy`, `filepath`,
  `status`) are unchanged.
- Passwords are hashed with `bcrypt` exactly as before.
- JWTs are signed with `PyJWT` using the same payload shape.
- File uploads use Flask's `request.files` + `secure_filename` in place of
  `multer`, keeping the `<timestamp>-<original-filename>` naming scheme and
  the `/uploads/...` public path.
