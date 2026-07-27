# Complaint management frontend

React + Redux Toolkit frontend for the AI-powered complaint management system.
Built with Vite.

## Setup

```bash
npm install
cp .env.example .env
# set VITE_API_URL if your backend isn't on localhost:8000
```

## Run

```bash
npm run dev
```

Opens on `http://localhost:5173`. The backend must be running for uploads,
analysis, and saving complaints to work — see `../backend/README.md`.

## Structure

```
src/
  main.jsx                    entry point, wraps App in the Redux Provider
  App.jsx                     header + tab switching (new complaint / list)
  index.css                   design tokens + all component styles
  api/
    client.js                 axios instance (base URL from VITE_API_URL)
  store/
    store.js                  combines the three slices below
    complaintFormSlice.js     form field state, tracks which fields were AI-filled
    aiCopilotSlice.js         upload/analyze async thunks + AI result state
    complaintsListSlice.js    fetch/save complaints against the backend
  components/
    ComplaintForm.jsx         the intake form (left column)
    AiCopilotPanel.jsx        paste/upload + analyze + "fill form" (right column)
    ComplaintsList.jsx        table view of saved complaints
    RiskBadge.jsx             small colored badge for risk level
```

## How the AI flow works in the UI

1. User pastes complaint text into the copilot panel, or uploads a file
   (which calls `POST /api/upload` to extract text first).
2. "Analyze complaint" calls `POST /api/analyze` and shows the AI's
   summary, risk level, missing fields, and duplicate warning.
3. "Fill form with AI results" dispatches `fillFromAi`, which populates
   the form on the left — those fields get a blue highlight
   (`.ai-filled` in `index.css`) until the user edits them, so it's
   visually clear what the AI supplied vs. what's user-verified.
4. "Save complaint" posts the final (possibly edited) form to
   `POST /api/complaints`.
