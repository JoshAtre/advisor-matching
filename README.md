# Advisor–Advisee Matching Tool

A full-stack MVP for matching students with research advisors based on interests and goals.

## Tech Stack
- **Frontend:** Next.js 14 (App Router), Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Matching:** Keyword vector similarity (Cosine Similarity)

## How to Run

### 1. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py  # Loads initial advisor data
uvicorn main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 to view the app.
