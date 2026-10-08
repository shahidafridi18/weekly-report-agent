# Weekly Report Agent — corrected startup guide

## 1. Backend

From the `backend` directory on your Mac:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Check http://localhost:8000/health and http://localhost:8000/docs.

Copy the weekly Excel files into `backend/data/weekly/`. The provided sample files are already there.
If you want Gemini insights, create `backend/.env` from `.env.example` and supply your own key. Without it, comparisons can still run with the AI option disabled.

## 2. Frontend

In a separate terminal, from the `frontend` directory:

```bash
npm install
npm run dev
```

Open the Vite URL displayed in the terminal (typically http://localhost:5173).

Keep `VITE_API_BASE_URL` empty to use the `/api` development proxy to port 8000. Do not restore a macOS `node_modules` folder from the old ZIP; install packages afresh.

## Important behavior

- The file picker lists files already inside `backend/data/weekly/`; it is not an upload form.
- After a successful comparison, the report button uses the same filenames and comparison parameters.
- Report history contains reports generated during the current app session; the backend does not expose an API to list or delete stored reports.
- A successful TypeScript check was run. A full production bundle and backend execution could not be verified in the Linux review environment because of platform-specific bundled dependencies and absent Python packages.
