# NCRB Drishti

Secure Digital Document Management System for legal and investigation documents (Smart India Hackathon problem **26190**, NCRB / Ministry of Home Affairs).

This repository is a **Django REST backend**. There is no web frontend in the current codebase. `Theme.md` is a UI design document only; it is not implemented.

The system stores cases and documents, authenticates users with JWT, records a local hash-based integrity trail (mock blockchain), writes document audit logs, and can optionally index uploaded files for RAG. RAG search/Q&A is library code only: there is no public RAG query API yet.

## Features currently implemented

- User registration and JWT login (`email` + password)
- Organizations, users, roles, and RBAC permission tables
- Case CRUD, status changes, assigned-case list, and case statistics
- Document upload, version upload, download, integrity verify, list, and soft delete
- SHA-256 hashing of stored files
- Local mock blockchain records (hash of `document_id:version_number:sha256`)
- Document audit logs for `upload`, `version_upload`, `download`, `verify`, and `delete`
- Optional RAG pipeline on upload (extract → chunk → embed → FAISS). Failures do not block storage.
- Django admin for organizations, users, roles, cases, and documents (users with `role=ADMIN`)

## Tech stack

| Layer | Actual implementation |
| --- | --- |
| Language | Python 3 |
| Framework | Django 6.1, Django REST Framework 3.18 |
| Auth | Custom user model (`ncrb_auth.User`), SimpleJWT |
| Database | PingCAP TiDB via `django-tidb` when `TIDB_HOST` is set; otherwise SQLite (`db.sqlite3`). Tests always use in-memory SQLite. |
| Files | Django `FileField` under `media/documents/` |
| Integrity | SHA-256 + local mock blockchain table |
| RAG (optional) | pypdf, optional python-docx / EasyOCR / Whisper / sentence-transformers / FAISS / Groq |

There is no React/Vue app, no Celery worker, and no external blockchain network in this codebase.

## Project structure

```text
NCRB-Drishti/
├── manage.py
├── requirements.txt
├── .env.example
├── check_tidb.py                # standalone TiDB TLS connectivity check
├── Theme.md                     # design system notes (not used by the app)
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── apps/
    ├── auth/                    # users, organizations, RBAC, JWT login/register
    ├── cases/                   # case API
    ├── documents/               # document API, hash/audit/blockchain services
    ├── RAG/                     # extractors, chunking, embeddings, FAISS, Groq client
    ├── audit/                   # empty Django app (no URLs/models)
    └── blockchain/              # empty Django app (no URLs/models)
```

`apps.audit` and `apps.blockchain` are **not** in `INSTALLED_APPS`. Audit and blockchain behaviour lives on `apps.documents` models (`AuditLog`, `BlockchainRecord`).

## Setup and installation

```bash
git clone <repository-url>
cd NCRB-Drishti
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Edit `.env` as needed. For local development you can leave `TIDB_HOST` empty and use SQLite.

Then:

```bash
python manage.py migrate
python manage.py runserver
```

The API is at `http://127.0.0.1:8000`. `/` redirects to `/documents/`.

## Environment variables

Loaded from `.env` via `python-dotenv`.

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret. Falls back to a development insecure key if unset. |
| `DJANGO_DEBUG` | `True`/`False`. Defaults to `True`. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts. Default: `127.0.0.1,localhost,testserver`. |
| `TIDB_HOST` | If set, Django uses TiDB. If empty, SQLite. |
| `TIDB_PORT` | Default `4000`. |
| `TIDB_USER` | TiDB user. |
| `TIDB_PASSWORD` | TiDB password. |
| `TIDB_DATABASE` | TiDB database name. |
| `TIDB_CA_PATH` | Path to TLS CA file for TiDB. |
| `GROQ_API_KEY` | Optional. Required only if you instantiate `GroqLLMService`. |
| `GROQ_MODEL` | Optional. Default `llama-3.3-70b-versatile`. |

Do not commit `.env`. A CA file such as `isrgrootx1.pem` is gitignored.

## Database setup

### SQLite (local default)

Leave `TIDB_HOST` unset or empty. Run `python manage.py migrate`. Data is stored in `db.sqlite3`.

### TiDB

1. Create a database and user on TiDB Cloud or a self-hosted cluster.
2. Download the CA certificate and set `TIDB_CA_PATH`.
3. Fill `TIDB_*` variables in `.env`.
4. Optional connectivity check: `python check_tidb.py`
5. `python manage.py migrate`

### Bootstrap data

Registration requires an existing organization. Creating organizations via API requires JWT plus RBAC permission `ORG_VIEW`. Typical first-time setup in the Django shell:

```bash
python manage.py shell
```

```python
from apps.auth.models import Organization, User, Role, Permission, UserRole, RolePermission

org = Organization.objects.create(
    org_code="PS-DEL-001",
    org_name="Delhi Central Police Station",
    org_type="POLICE_STATION",
)

admin = User.objects.create_user(
    email="admin@example.com",
    password="ChangeThisPassword!2026",
    organization=org,
    employee_code="EMP-ADMIN",
    full_name="System Admin",
    role=User.Role.ADMIN,
)

role = Role.objects.create(code=Role.RoleCode.DEPARTMENT_ADMIN, name="Department Admin")
perm = Permission.objects.create(code="ORG_VIEW", name="View organizations")
RolePermission.objects.create(role=role, permission=perm)
UserRole.objects.create(user=admin, role=role)
```

Django admin is at `/admin/`. Only users with `role=ADMIN` are staff. There is no `createsuperuser` flow that bypasses `organization` (the custom user requires an organization).

## How to run

```bash
python manage.py runserver
```

Use `Authorization: Bearer <access-token>` on authenticated routes. Access tokens last **30 minutes**. Refresh tokens last **1 day**. There is **no token-refresh API** in this project; log in again when the access token expires.

JSON bodies use `Content-Type: application/json`. File uploads use multipart form-data.

## API endpoints

Base URL: `http://127.0.0.1:8000`

### Auth — ` /api/auth/`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET, POST | `/api/auth/organizations/` | JWT + RBAC `ORG_VIEW` | List or create organizations |
| POST | `/api/auth/register/` | none | Register a user against an existing organization |
| GET | `/api/auth/login/` | none | Help text (not a session login form) |
| POST | `/api/auth/login/` | none | Returns JWT `access` and `refresh` |

Register body:

```json
{
  "organization": 1,
  "employee_code": "EMP-1001",
  "full_name": "Asha Sharma",
  "email": "asha.sharma@example.com",
  "phone": "9876543210",
  "password": "AshaStrongPass!2026",
  "confirm_password": "AshaStrongPass!2026"
}
```

`org_type` must be one of `POLICE_STATION`, `COURT`, `NCRB`, `FORENSIC_LAB`, `LEGAL_DEPT`.

Login body:

```json
{
  "email": "asha.sharma@example.com",
  "password": "AshaStrongPass!2026"
}
```

Default user `role` on register is `OFFICER`. MFA columns exist but are unused.

### Cases — `/api/cases/`

All case routes require JWT. List/retrieve/documents/stats/my_cases: any authenticated user, scoped by `CaseService.get_user_cases`:

- `ADMIN`: all cases
- `OFFICER`: cases they created or are assigned to
- other roles: cases in their organization

Create / update / `change_status`: user `role` must be `ADMIN` or `OFFICER`. Officers may edit only their own created/assigned cases. Delete: `ADMIN` only.

| Method | Path |
| --- | --- |
| GET, POST | `/api/cases/cases/` |
| GET, PUT, PATCH, DELETE | `/api/cases/cases/{id}/` |
| POST | `/api/cases/cases/{id}/change_status/` |
| GET | `/api/cases/cases/{id}/documents/` |
| GET | `/api/cases/cases/my_cases/` |
| GET | `/api/cases/cases/stats/` |

List query parameters: `status`, `priority`, `case_type`, `search`.

Create example:

```json
{
  "fir_number": "FIR-DEL-2026-0001",
  "title": "Central Delhi burglary investigation",
  "description": "Investigation into a reported residential burglary.",
  "case_type": "INVESTIGATION",
  "status": "OPEN",
  "priority": "HIGH",
  "organization": 1,
  "assigned_officer": 1
}
```

`case_type`: `CRIMINAL`, `CIVIL`, `INVESTIGATION`.  
`status`: `OPEN`, `UNDER_INVESTIGATION`, `CHARGESHEETED`, `IN_TRIAL`, `CLOSED`, `ARCHIVED`.  
`priority`: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.  
`case_number` is generated as `NCRB/<8 hex chars>`.

### Documents — `/documents/`

JWT required. Access is limited to documents whose case is visible to the user (same scoping as cases).

| Method | Path | Body |
| --- | --- | --- |
| GET | `/documents/` | — |
| POST | `/documents/upload/` | multipart: `case_id`, `title`, `description` (optional), `file` |
| POST | `/documents/{document_id}/versions/upload/` | multipart: `file` |
| GET | `/documents/{version_id}/download/` | file attachment |
| GET | `/documents/{version_id}/verify/` | JSON verification result |
| POST | `/documents/{document_id}/delete/` | soft delete |

Note the ID types: download/verify take a **version** id; delete and version-upload take a **document** id.

### Audit and blockchain APIs

There are no `/audit/` or `/blockchain/` HTTP routes. Inspect `documents_auditlog` / `documents_blockchainrecord` (SQLite) or the corresponding TiDB tables, or use verify/download responses.

## Important workflows

```text
Organization exists
        → POST /api/auth/register/
        → POST /api/auth/login/  (JWT)
        → POST /api/cases/cases/
        → POST /documents/upload/
             → optional RAG index
             → SHA-256
             → Document + DocumentVersion
             → mock BlockchainRecord
             → AuditLog (upload)
        → GET /documents/{version_id}/verify/
             → re-hash file, compare stored hashes
```

Integrity verification is **local**. It does not submit a transaction to Bitcoin, Ethereum, or any other chain.

## Dependencies

From `requirements.txt`:

- Django, djangorestframework, djangorestframework_simplejwt
- django-tidb, PyMySQL, python-dotenv
- django-filter, pillow, pypdf, reportlab
- asgiref, sqlparse, tzdata, charset-normalizer, PyJWT

Optional RAG extras (not in `requirements.txt`; install only if you need indexing):

- `python-docx` for `.docx`
- `pymupdf` is not required; PDFs use `pypdf`
- `easyocr` for images
- `openai-whisper` for audio
- `langchain-text-splitters` (a simple splitter is used if this is missing)
- `sentence-transformers`, `faiss-cpu`, `numpy`
- `groq` for `apps/RAG/LLM/client.py`

## Testing

```bash
python manage.py test
```

Tests use in-memory SQLite even if TiDB is configured, so they will not touch the remote database.

Covered areas include registration/login, organization RBAC, case creation, JWT document upload/verify/download, and cross-organization access denial.

## Known limitations

- No frontend; API-only.
- No JWT refresh endpoint (`ROTATE_REFRESH_TOKENS` is off; blacklist app is not installed).
- Organization API cannot be used until at least one user has `ORG_VIEW` via `UserRole` / `RolePermission`.
- Two role systems exist: `User.role` (`ADMIN`, `OFFICER`, …) for cases, and `Role`/`UserRole` tables for `ORG_VIEW`. They are not synced.
- Blockchain is a local SHA-256 mock.
- RAG has no query/chat endpoint. FAISS files are written under `apps/RAG/vectorstore_data/` when indexing succeeds.
- `apps/audit` and `apps/blockchain` are stubs.
- MFA, email sending, and digital signatures are not implemented (`EMAIL_BACKEND` is console).
- Media files are served only when `DEBUG` is true.
- Default `DJANGO_SECRET_KEY` is insecure if you do not set one.

## Important commands

```bash
python -m venv venv
pip install -r requirements.txt
python check_tidb.py
python manage.py migrate
python manage.py showmigrations
python manage.py shell
python manage.py runserver
python manage.py test
python manage.py createsuperuser   # still requires an organization id
```

## Notes for new developers and agents

- Custom user app label is `ncrb_auth`, table `users`, password column `password_hash`.
- Do not assume session cookies authenticate the API. Use JWT.
- Do not invent `/audit/` or `/rag/ask/` routes; they are not wired.
- Keep document upload working even when RAG libraries are absent.
- `config/urls.py` already includes `api/auth/` and `api/cases/` (older README text about DEBUG-only wiring is obsolete).
