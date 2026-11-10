# AI Pharma Complaint Management System

An AI-assisted pharmaceutical complaint management system designed to simplify complaint intake, information extraction, and preliminary risk assessment. The system processes complaint information from emails, PDF documents, or text input and helps reviewers organize and evaluate cases more efficiently.

## 📌 Project Overview

Pharmaceutical complaint handling involves reviewing customer reports, identifying relevant product and batch information, assessing potential risks, and ensuring that important details are captured for further investigation.

This project explores how Artificial Intelligence can assist this workflow by converting unstructured complaint information into structured records, generating summaries, identifying missing information, and flagging potential duplicate complaints.

The system is designed to support human reviewers by reducing repetitive manual work and helping them make more informed decisions.

## ✨ Key Features

- **Complaint Intake:** Accepts complaint information from emails, PDF documents, and text input.
- **AI-Based Information Extraction:** Extracts relevant details from unstructured complaint descriptions.
- **Complaint Summarization:** Generates concise summaries to help reviewers understand reported issues.
- **Preliminary Risk Assessment:** Assists in identifying the potential risk associated with a complaint.
- **Missing Information Detection:** Highlights important complaint details that may require additional information.
- **Duplicate Complaint Detection:** Flags potentially duplicate cases for further review.
- **Structured Complaint Management:** Organizes extracted information to support complaint review and follow-up.

## 🏗️ System Architecture

The project is organized into two main components:

```text
AI Pharma Complaint Management
│
├── frontend/
│   └── User interface for complaint
│       intake and review
│
├── backend/
│   └── Complaint processing,
│       AI integration, and
│       application logic
│
└── README.md
```

The frontend provides the user-facing interface, while the backend handles the application logic and AI-assisted complaint processing.

## 🛠️ Technology Stack

The application is organized as a frontend-backend system with AI-assisted processing.

- **Frontend:** User interface for submitting and reviewing complaints.
- **Backend:** Application logic and complaint processing.
- **Artificial Intelligence:** Information extraction, summarization, and preliminary risk assessment.
- **Document Processing:** Support for complaint information provided through emails, PDFs, and text.

*Note: Refer to the frontend and backend source files for the exact frameworks, libraries, AI models, and dependencies used in this implementation.*

## 🎯 Project Objectives

- Explore practical applications of AI in pharmaceutical complaint management.
- Reduce repetitive manual effort during complaint intake.
- Convert unstructured complaint information into organized records.
- Support preliminary risk identification and complaint prioritization.
- Improve the identification of missing information and potential duplicate cases.
- Demonstrate the integration of AI capabilities into a software application.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (a local database, e.g. `complaints_db`)
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
git clone https://github.com/sandeepklr12345-gif/AI-Pharma-Complaint-Management.git
cd AI-Pharma-Complaint-Management
```

**Backend** (http://localhost:8000, API docs at `/docs`)

```bash
cd backend
python -m venv venv && source venv/bin/activate    # Windows: venv\Scriptsctivate
pip install -r requirements.txt
cp .env.example .env                                # then set GROQ_API_KEY and DATABASE_URL
createdb complaints_db                              # tables are created on first run
uvicorn app.main:app --reload --port 8000
```

**Frontend** (http://localhost:5173)

```bash
cd frontend
cp .env.example .env                                # VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

### Tests and CI

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

The tests run without Groq, Postgres or the embedding model: the LLM, database and embedder are replaced by fakes.
They cover JSON clean-up of model output, the completeness check, risk classification, duplicate detection thresholds
and file upload handling. GitHub Actions runs the backend tests and a frontend build on every push and pull request.

## 🔍 Example Workflow

1. Submit a customer complaint through an email, PDF document, or text input.
2. Process the complaint information using the application's AI-assisted workflow.
3. Extract relevant complaint details and generate a summary.
4. Review the preliminary risk assessment.
5. Identify missing information and potential duplicate cases.
6. Review the results and determine the appropriate next steps.

## ⚠️ Scope and Limitations

- AI-generated information and risk assessments require human review.
- Duplicate detection results should be verified before treating complaints as duplicates.
- The system is intended to assist complaint handling, not replace qualified pharmaceutical quality assurance professionals.
- AI-generated assessments do not independently establish regulatory compliance or replace formal investigation and reporting procedures.


---

*An AI-assisted software project exploring the application of artificial intelligence to pharmaceutical complaint intake and review.*
