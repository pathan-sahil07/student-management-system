# 🎓 Student Management System

A full-stack **Student Management System** built with **Nuxt.js 3** (Vue 3 Composition API) on the frontend and **FastAPI** on the backend. The project demonstrates clean architecture, REST API design, form validation, and a modern, responsive UI.

---

## ✨ Features

### Frontend (Nuxt.js 3)
- Vue 3 Composition API (`<script setup>`) throughout
- Responsive sidebar navigation with mobile drawer
- **Dashboard** — total students, course count, average year, recently added students
- **Students** page — searchable, paginated table with edit/delete actions
- **Add Student** page — validated form with success feedback
- **Edit Student** page — pre-filled form, update in place
- Reusable components: `StudentForm`, `ConfirmDialog`, `LoadingSpinner`, `ToastContainer`, `StatCard`, `EmptyState`, `AppSidebar`, `AppTopbar`
- Client-side form validation (required fields, email format, phone format, year range)
- Toast notifications for success/error states
- Loading spinners during API calls
- Delete confirmation dialog
- Clean, modern, light-themed, fully responsive UI (desktop + mobile)

### Backend (FastAPI)
- RESTful CRUD API for student records
- Pydantic v2 models with field-level validation
- Modular project structure (`models.py`, `schemas.py`, `routes.py`, `config.py`, `database.py`)
- CORS enabled for the Nuxt frontend
- Proper HTTP status codes (200, 201, 404, 409, 422, 500)
- Centralized exception handling
- Auto-generated Swagger (`/docs`) and ReDoc (`/redoc`) documentation
- In-memory data store (Python list) seeded with sample data — designed to be swapped for SQLite with minimal changes (see `database.py`)

---

## 📁 Project Structure

```
student-management-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app, middleware, exception handlers
│   │   ├── models.py          # In-memory data store (Student dataclass + StudentDB)
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── routes.py          # CRUD API route handlers
│   │   ├── database.py        # Placeholder / migration guide for SQLite
│   │   ├── config.py          # App settings (CORS origins, etc.)
│   │   └── requirements.txt
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── components/
    │   ├── AppSidebar.vue
    │   ├── AppTopbar.vue
    │   ├── StudentForm.vue
    │   ├── ConfirmDialog.vue
    │   ├── LoadingSpinner.vue
    │   ├── ToastContainer.vue
    │   ├── StatCard.vue
    │   └── EmptyState.vue
    ├── composables/
    │   ├── useStudentsApi.ts  # All HTTP calls to the backend
    │   └── useToast.ts        # Global toast notification state
    ├── pages/
    │   ├── index.vue          # Dashboard
    │   └── students/
    │       ├── index.vue      # Students list (search, pagination, delete)
    │       ├── add.vue        # Add student form
    │       └── edit/[id].vue  # Edit student form
    ├── assets/css/main.css    # Design tokens + global styles
    ├── public/favicon.svg
    ├── app.vue
    ├── nuxt.config.ts
    └── package.json
```

---

## 🚀 Getting Started

### Prerequisites
- **Python** 3.10+
- **Node.js** 18+ and npm
- (Optional) `virtualenv` for isolating Python dependencies

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Activate the virtual environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**
Swagger docs: **http://localhost:8000/docs**
ReDoc docs: **http://localhost:8000/redoc**

### 2. Frontend Setup

Open a **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at **http://localhost:3000**

> The frontend is pre-configured to call the backend at `http://localhost:8000` (see `runtimeConfig.public.apiBase` in `nuxt.config.ts`). Override it with the `NUXT_PUBLIC_API_BASE` environment variable if you deploy the backend elsewhere.

### 3. Open the App
Visit **http://localhost:3000** in your browser. The backend starts pre-seeded with 5 sample students so the dashboard and table are populated immediately.

---

## 📡 API Documentation

Base URL: `http://localhost:8000`

| Method | Endpoint              | Description                          | Success Status |
|--------|------------------------|---------------------------------------|-----------------|
| GET    | `/students`            | List all students (supports `?search=`) | 200 |
| GET    | `/students/{id}`       | Get a single student by ID            | 200 |
| POST   | `/students`            | Create a new student                  | 201 |
| PUT    | `/students/{id}`       | Update an existing student (partial)  | 200 |
| DELETE | `/students/{id}`       | Delete a student                      | 200 |

**Error responses** use standard status codes:
- `404` — Student not found
- `409` — Email already registered
- `422` — Validation error (e.g. invalid email, year out of range)
- `500` — Unexpected server error

### Student Model

```json
{
  "id": 1,
  "name": "Aarav Sharma",
  "email": "aarav.sharma@example.com",
  "course": "Computer Science",
  "year": 2,
  "phone": "9876543210"
}
```

### Example Requests

**Create a student**
```bash
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane.doe@example.com","course":"Computer Science","year":2,"phone":"9876543210"}'
```

**Search students**
```bash
curl "http://localhost:8000/students?search=computer"
```

**Update a student**
```bash
curl -X PUT http://localhost:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"year":3}'
```

**Delete a student**
```bash
curl -X DELETE http://localhost:8000/students/1
```

Full interactive documentation with request/response schemas is available at `/docs` once the backend is running.

---

## 🗄️ Switching to SQLite

The project currently uses an in-memory Python list (`backend/app/models.py`) so it runs with **zero database setup**. To persist data with SQLite:

1. Add `sqlalchemy` to `requirements.txt`.
2. Implement SQLAlchemy models and a session factory in `backend/app/database.py` (a guide is already commented in that file).
3. Replace the body of the `StudentDB` class methods in `models.py` with SQLAlchemy queries (the public method signatures — `get_all`, `get_by_id`, `create`, `update`, `delete` — should stay the same so `routes.py` requires no changes).
4. Set `USE_DATABASE=True` in `.env` (copy `.env.example` to `.env` first).

---

## 🎨 UI Notes

- **Theme:** light, professional, indigo accent color (`#4f5fff`)
- **Typography:** Inter (loaded via Google Fonts)
- **Responsive breakpoints:** sidebar collapses to a drawer below 900px; forms and tables reflow on small screens
- **Components are intentionally framework-agnostic** in their styling (scoped CSS using shared design tokens defined in `assets/css/main.css`), making them easy to restyle or migrate to a UI library later

---

## 🧪 Tested Functionality

- ✅ Backend CRUD endpoints verified via `curl` (create, read, update, delete, search, 404/409 handling)
- ✅ Frontend build (`npm run build`) completes successfully
- ✅ All pages (`/`, `/students`, `/students/add`, `/students/edit/:id`) render correctly
- ✅ Form validation blocks submission on invalid input and surfaces inline errors
- ✅ Toast notifications fire on success/error for create, update, and delete actions
- ✅ Delete requires confirmation via modal dialog

---

## 📸 Screenshots (Description)

Since this is a generated project, here's what each page looks like:

- **Dashboard** — Three stat cards (Total Students, Courses Offered, Average Year) at the top, followed by a card listing the 5 most recently added students with avatar initials, course badges, and year badges.
- **Students** — A search bar with live filtering, a clean data table with avatar/name/email/course/year/phone columns, edit and delete icon buttons per row, and numbered pagination at the bottom.
- **Add Student** — A two-column responsive form (name/email, course/year, phone full-width) with inline validation messages and a primary "Add Student" submit button.
- **Edit Student** — Same form layout as Add, pre-filled with the selected student's current data, with an "Update Student" button.
- **Delete Confirmation** — A centered modal with a warning icon asking the user to confirm before permanently deleting a record.

---

## 🛠️ Tech Stack

| Layer       | Technology |
|-------------|------------|
| Frontend    | Nuxt.js 3, Vue 3 (Composition API), TypeScript |
| Backend     | FastAPI, Pydantic v2, Uvicorn |
| Styling     | Custom CSS with design tokens (no UI framework dependency) |
| HTTP Client | Nuxt's built-in `$fetch` (ofetch, built on the native Fetch API) |
| Data Store  | In-memory Python list (SQLite-ready architecture) |

---

## 📄 License

This project is provided as-is for educational/demonstration purposes.
