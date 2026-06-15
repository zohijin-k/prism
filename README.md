# PRISM

**Paper Reproduction & Implementation Specification Manager**

PRISM is a web service that analyzes a research paper PDF alongside optional GitHub repository or ZIP code, then returns a structured breakdown across six dimensions:

1. **Paper Summary** — Problem, limitation, method, result, contributions
2. **Implementation Plan** — Step-by-step reproduction roadmap
3. **Research Components** — Dataset, model, loss, optimizer, metrics, hyperparameters
4. **Paper-Code Comparison** — Side-by-side alignment table with match status
5. **Paper-Code Mapping** — Fine-grained mapping from code blocks to paper sections
6. **Missing Info** — Gaps in the paper's reproducibility

## Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend  | FastAPI + Python 3.11               |
| Analysis | Mock (LLM integration planned)      |

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Environment Variables

Copy `.env.example` to `.env` and fill in values before running.

## Project Structure

```
PRISM/
├── backend/
│   ├── main.py               # FastAPI app + CORS
│   ├── mock_data.py          # Mock analysis response
│   ├── routers/
│   │   └── analyze.py        # POST /api/analyze
│   └── models/
│       └── schemas.py        # Pydantic response models
└── frontend/
    └── src/
        ├── App.tsx
        ├── api.ts
        ├── types.ts
        └── components/
            ├── UploadForm.tsx
            ├── ResultTabs.tsx
            └── tabs/          # One component per result tab
```
