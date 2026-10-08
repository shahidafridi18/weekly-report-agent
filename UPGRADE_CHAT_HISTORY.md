# Weekly Report Agent: Chat history and report naming update

This patch changes both `frontend` and `backend`. Apply the paths in the ZIP over the
matching files in your existing project, preserving the directory structure.

## Before applying

- Keep your existing `backend/.env` and `backend/data/` folder, especially
  `backend/data/agent_sessions.sqlite3`. **Do not delete the database.**
- Back up the files being replaced if you have made additional local changes.
- Stop your FastAPI and Vite development servers.

## After applying

1. Start FastAPI from the existing `backend` folder:
   `uvicorn app.main:app --reload --port 8000`
2. Start Vite from `frontend`: `npm run dev`.
3. Open the Chat page. Existing conversations appear in the History panel.
4. Click **New chat**, send a message, then click the older conversation to
   restore it and continue under the original session ID.
5. Generate a new PDF/XLSX report and download it. The saved filename should
   match the display name in the report card.

No dependency reinstall or database reset is required.

## Compatibility and limits

- Existing SQLite sessions are preserved. Old sessions only have up to six
  previously recorded exchanges; earlier turns were never stored in full.
- New exchanges use a separate `agent_turns` SQLite table, retaining the full
  chat text while the AI still receives its bounded context.
- Sessions expire after 30 days of inactivity by default. Previously deleted
  or expired sessions cannot be recovered.
- The backend now exposes `GET /api/agent/sessions` and includes a `turns`
  array in `GET /api/agent/sessions/{session_id}`.
- Newly generated reports persist their readable filenames alongside the
  report files. Old report links can use a validated `filename` query parameter.
- The app's session endpoints have no account authentication. Add user-scoped
  authentication before exposing this backend to other users or the Internet.
