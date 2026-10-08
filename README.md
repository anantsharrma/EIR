# EIR

> **An intelligent patient history-taking assistant for OPDs**

EIR is an early-stage healthcare software project designed to help streamline **patient history taking** in outpatient departments (OPDs).

Instead of spending valuable consultation time collecting a patient's history from scratch, EIR guides the patient through a structured conversation, organizes the information, and prepares it for **physician review and verification**.

> Project Status: Early-stage prototype / v0.1.0
> EIR is currently a software prototype and in its building stage.

---

## The Problem

In busy OPDs, doctors often have only a few minutes with each patient.

A significant portion of that time can be spent collecting and organizing information such as:

* Chief complaints
* History of present illness
* Previous illnesses and surgeries
* Medications and allergies
* Family history
* Personal history
* Review of systems

Patients may also forget relevant details, describe symptoms inconsistently, or remember important past events only after the consultation has started.

This creates a simple problem:

**Doctors need structured information, but collecting that information takes time.**

---

## The Idea

EIR acts as a **pre-consultation history-taking assistant**.

The basic workflow is:

```text
Patient
   ↓
EIR asks relevant questions
   ↓
Patient provides answers
   ↓
Information is extracted & structured
   ↓
History is organized into a case sheet
   ↓
Doctor reviews & verifies
   ↓
Consultation
```

The goal is not to replace the doctor.

The goal is to make the information reaching the doctor **more complete, structured, and easier to review**.

---

## Current Prototype

The current version focuses on building the underlying workflow before adding more sophisticated AI capabilities.

### v0.1.0

Currently implemented:

* Patient creation
* Session creation
* Basic FastAPI backend
* Initial API workflow
* Early session/patient data handling

Currently being developed:

* History-taking state management
* Question flow / orchestrator
* Patient response handling
* Structured history extraction
* Section-wise history collection
* Doctor handoff / case-sheet generation

Future versions may introduce:

* LLM-assisted information extraction
* Intelligent follow-up questions
* Medical terminology normalization
* Verification of extracted information
* Multilingual interaction
* Voice-based interaction
* OCR/document ingestion
* Doctor dashboard
* ABDM/ABHA integration where appropriate

---

## Architecture Direction

EIR is being designed around a **controlled workflow rather than a completely free-form chatbot**.

The intended architecture is approximately:

```text
                    ┌────────────────────┐
                    │     Patient UI     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Orchestrator    │
                    │  Controls workflow │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   State Manager    │
                    │ Session + progress │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Extraction Engine  │
                    │  Structured data   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Normalization &    │
                    │    Verification    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Case Sheet      │
                    │  Doctor Review     │
                    └────────────────────┘
```

A key design principle is that **the LLM should assist the workflow, not control the entire workflow**.

The application should know which section it is currently collecting, what information is still required, and what happens next.

---

## Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Pydantic**
* Async API architecture

### Planned / Exploring

* PostgreSQL
* SQLAlchemy
* Alembic
* LLM APIs
* React
* Tailwind CSS

The stack is intentionally evolving as the prototype develops.

---

## Project Structure

The project is currently being organized around a backend-first architecture.

```text
eir/
│
├── src/
│   └── ...
│
├── main.py
├── app.py
├── pyproject.toml
├── .gitignore
└── README.md
```

As the project grows, the backend will be separated into clearer modules for:

```text
API
├── Patients
├── Sessions
└── History

Core
├── Orchestrator
├── State Manager
└── Schemas

AI
├── Extraction
├── Normalization
└── Verification
```

The structure is expected to change during development.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/eir.git
cd eir
```

### 2. Install dependencies

This project uses `uv` for Python environment and dependency management.

```bash
uv sync
```

### 3. Start the application

```bash
uv run main.py
```

The API should then be available locally.

FastAPI's interactive API documentation can be accessed at:

```text
http://127.0.0.1:8000/docs
```

---

## Current API

The current prototype exposes basic endpoints for creating patients and sessions.

### Create Patient

```http
POST /patients
```

### Create Session

```http
POST /sessions
```

The API design will evolve as the state-management and history-taking workflow is implemented.

---

## Design Principles

### 1. Doctor-in-the-loop

EIR does not make the final clinical decision.

The physician remains responsible for reviewing and interpreting the collected history.

### 2. Structured over free-form

Rather than treating the system as a generic chatbot, EIR aims to collect information according to a defined clinical workflow.

### 3. One step at a time

The patient should not be overwhelmed with a large form.

The system should progressively collect information through focused questions.

### 4. AI where it adds value

AI should be used for tasks such as:

* Understanding natural-language responses
* Extracting structured information
* Identifying potentially relevant details
* Normalizing terminology
* Generating appropriate follow-up questions

Deterministic application logic should handle workflow and state wherever possible.

### 5. Patient information comes first

The system should preserve what the patient actually reports rather than silently inventing or assuming clinical information.

---

## What EIR Is Not

EIR is **not currently**:

* A diagnostic system
* A replacement for a doctor
* An autonomous clinical decision-maker
* A prescription system
* A medical emergency response system

The prototype is focused specifically on **history collection and organization**.

---

## Roadmap

### Phase 1 — Workflow Foundation

* [x] FastAPI application
* [x] Patient creation
* [x] Session creation
* [ ] Session state management
* [ ] Question orchestration
* [ ] Patient response handling

### Phase 2 — Structured History

* [ ] History schemas
* [ ] Section-wise collection
* [ ] Response extraction
* [ ] Data normalization
* [ ] Verification layer

### Phase 3 — AI Integration

* [ ] LLM extraction
* [ ] Intelligent follow-up questions
* [ ] Context-aware questioning
* [ ] Structured case-sheet generation

### Phase 4 — Patient & Doctor Interfaces

* [ ] Patient interface
* [ ] Doctor review interface
* [ ] History editing
* [ ] Consultation handoff

### Phase 5 — Advanced Features

* [ ] Multilingual support
* [ ] Voice interaction
* [ ] Document/OCR ingestion
* [ ] Healthcare ecosystem integrations
* [ ] Security and production hardening

---

## Current Status

**EIR is actively being developed.**

The current priority is to build a reliable **history-taking workflow and backend foundation** before adding advanced AI capabilities.

The project will evolve iteratively from:

```text
Workflow
   ↓
State Management
   ↓
Structured History
   ↓
AI Assistance
   ↓
Patient Interface
   ↓
Doctor Interface
   ↓
Production Readiness
```

---

## Disclaimer

EIR is an experimental software project intended for development and demonstration purposes.

It should not be used to make medical decisions or provide medical advice. Any future clinical deployment would require appropriate medical validation, privacy/security controls, regulatory compliance, and professional oversight.

---

