# Contract Worker Management System

A beginner-friendly full-stack app using **FastAPI + Jinja2 + MySQL**.

## Features

- Add contract workers with name, contract dates, and photo upload.
- Auto-generate unique `worker_code`.
- Auto-generate QR code based only on `worker_code` (no sensitive data).
- Attendance scan endpoint (`/scan`) toggles `IN` and `OUT`.
- Cooldown logic prevents fast duplicate scans.
- Server-rendered UI (no React):
  - Add Worker page
  - View Workers page with photo + QR
- Contract expiry indicator in table and API response.

## Project Structure

```text
app/
├── main.py
├── database/
│   ├── connection.py
│   └── init_db.sql
├── models/
│   ├── __init__.py
│   ├── attendance_log.py
│   └── worker.py
├── routes/
│   ├── __init__.py
│   ├── api.py
│   └── web.py
├── services/
│   ├── attendance_service.py
│   ├── qr_service.py
│   └── worker_service.py
├── static/
│   ├── css/styles.css
│   ├── photos/
│   └── qrcodes/
└── templates/
    ├── add_worker.html
    ├── base.html
    └── workers.html
requirements.txt
```

## 1) Setup MySQL

Run SQL from `app/database/init_db.sql`:

```bash
mysql -u root -p < app/database/init_db.sql
```

## 2) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Configure database URL

Set environment variable:

```bash
export DATABASE_URL="mysql+mysqlconnector://root:password@localhost:3306/contract_management"
```

## 4) Run the app

```bash
uvicorn app.main:app --reload
```

Open:
- UI: `http://127.0.0.1:8000/`
- Scan API docs: `http://127.0.0.1:8000/docs`

## API Example: Scan Attendance

```bash
curl -X POST http://127.0.0.1:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"worker_code":"WRK-ABC12345"}'
```

Response includes:
- `type`: `IN` or `OUT`
- `contract_expired`: `true` or `false`

## Notes

- Photos are saved under `app/static/photos/`.
- QR files are saved under `app/static/qrcodes/`.
- SQLAlchemy auto-creates tables at startup (`Base.metadata.create_all`) if they do not exist.

## Images

<img width="1920" height="1080" alt="Screenshot (15)" src="https://github.com/user-attachments/assets/e2ac4b6c-c0ec-450c-9e8e-8287afb98d3f" />

<img width="1920" height="1080" alt="Screenshot (16)" src="https://github.com/user-attachments/assets/8405bcb9-b87a-4613-ab55-9da2f9112637" />


