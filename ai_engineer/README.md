# Interview Exercise

This repo contains a simplified version of a real AI-powered feature from our platform: a classifier that flags incoming user messages as urgent or not urgent so Wellthy's Care Team can prioritize them for review and/or escalation. The system accepts free-text input, runs a classification method, returns a label plus some idea of confidence and its rationale, and stores enough metadata for later evaluation.

"Urgent" means any message that needs to get in front of one of our Care Managers as soon as possible. So you can assume that:

1. Messages flagged as urgent will be prioritized for faster human review.
2. Missing a truly urgent message is  worse than over-flagging a non-urgent one.
3. Some messages are inherently ambiguous and may depend on our business policy

The repo includes:

* a minimal frontend and backend
* a simple model implementation
* a labeled evaluation dataset
* a basic evaluation script, and
* a sample log file representing production-like predictions

Please review the repo before the interview. You do not need to write code or prepare a formal presentation.

In the live interview, we will ask you questions and your thoughts about evaluating and monitoring this feature. We’re less interested in the specific classifier implementation than in how you think about evaluating and improving AI systems in practice, especially under realistic product and data constraints.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Backend Server**
   ```bash
   python3 -m uvicorn backend.app:app --reload
   ```
   The server will start on http://localhost:8000
   
   Note: On first run, the Hugging Face model (~1.6GB) will download automatically.

3. **Run the Frontend**
   The frontend is a Vite + React + TypeScript app (styled with Tailwind CSS) located in `frontend/`.

   Requirements: Node.js 20.19+ or 22.12+ (a `.nvmrc` pins `22.17.1` — run `nvm use` from the `frontend/` directory if you use nvm).

   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   The dev server starts on http://localhost:5173 and connects to the backend at `http://localhost:8000`. To point at a different backend, set `VITE_API_URL` (e.g. `VITE_API_URL=http://localhost:9000 npm run dev`).

   To produce a production build:
   ```bash
   npm run build
   npm run preview
   ```

4. **Run Evaluation (Optional)**
   ```bash
   python evaluation/eval.py
   ```
   This will evaluate the model on evaluation data (`data/eval_dataset.csv`) and generate a confusion matrix.

## Project Structure
```
ai_engineer/
├── README.md
├── ai/
│   ├── __init__.py
│   └── model.py
├── backend/
│   ├── __init__.py
│   └── app.py
├── data/
│   ├── eval_dataset.csv
│   └── logs.csv
├── evaluation/
│   ├── __init__.py
│   └── eval.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/classify.ts
│       └── components/
│           ├── MessageClassifier.tsx
│           └── ClassificationResult.tsx
└── requirements.txt
```

## API Endpoints

- `POST /classify`: Classify a message for urgency
  - Body: `{"text": "message content"}`
  - Response: 
    ```json
    {
      "urgent": true/false,
      "confidence_score": 0.0-1.0,
      "model_version": "string",
      "reasoning": "string"
    }
    ```

- `GET /health`: Health check endpoint
  - Response: `{"status": "healthy"}`

- `GET /logs`: Retrieve recent log entries
  - Query params: `lines=50` (default: 50 lines)
  - Response: 
    ```json
    {
      "total_lines": int,
      "returned_lines": int,
      "logs": ["array of log entries"]
    }
    ```

## Logging

Logs are written to `data/logs.csv` with the following columns:
- **timestamp**: When the log entry was created (YYYY-MM-DD HH:MM:SS)
- **logger**: Logger name/module
- **level**: Log level (INFO, ERROR, WARNING, etc.)
- **message**: Log message

View recent logs via:
1. **API endpoint**: `GET /logs?lines=50` (returns JSON)
2. **Direct file**: Open `data/logs.csv` with any text editor or spreadsheet application

This CSV format enables easy analysis, filtering, and integration with data tools.