# Complaint management backend

FastAPI + LangGraph + Groq backend for the AI-powered complaint management system.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# then fill in GROQ_API_KEY (free key at console.groq.com) and DATABASE_URL
```

Create the Postgres database referenced in `DATABASE_URL` (tables are created
automatically on first run via `Base.metadata.create_all`):

```bash
createdb complaints_db
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI) —
useful for testing `/api/analyze` before the frontend exists.

## How a request flows

1. `POST /api/upload` — user uploads a PDF or pasted email text, this
   endpoint extracts raw text and returns it (no AI involved yet).
2. `POST /api/analyze` — the extracted (or pasted) text goes into the
   LangGraph pipeline (`app/graph/pipeline.py`):
   - `extract_fields` pulls structured data out via Groq
   - four nodes run in parallel: `summarize`, `check_completeness`,
     `classify_risk`, `check_duplicate`
   - `finalize` is the join point before returning
3. The frontend shows the AI's output in the copilot panel; the user
   reviews/edits it, then `POST /api/complaints` persists the final record.

## Project layout

```
app/
  main.py           FastAPI app, CORS, router registration
  config.py         env-driven settings
  database.py       SQLAlchemy engine/session
  models.py         ORM models (complaints, complaint_attachments)
  schemas.py        Pydantic request/response models
  routers/
    upload.py       POST /api/upload
    analyze.py      POST /api/analyze
    complaints.py   CRUD for /api/complaints
  services/
    groq_client.py       Groq API wrapper + JSON-mode prompting helper
    text_extraction.py   PDF/email text extraction
  graph/
    state.py         ComplaintState TypedDict
    nodes.py          individual LangGraph node functions
    pipeline.py       wires nodes into the StateGraph (parallel fan-out)
```
