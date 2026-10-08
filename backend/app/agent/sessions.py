"""Small SQLite session records; selections/history persist, raw datasets do not."""
import json
from pathlib import Path
import sqlite3
from threading import RLock
import time
from uuid import uuid4


class SessionNotFoundError(LookupError):
    pass


class SessionConflictError(RuntimeError):
    pass


class SessionStore:
    def __init__(self, path: str | Path = ":memory:", ttl_seconds: int = 86400):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(path), timeout=10, check_same_thread=False)
        self.lock = RLock()
        self.ttl_seconds = ttl_seconds
        with self.connection:
            self.connection.execute("CREATE TABLE IF NOT EXISTS agent_sessions (id TEXT PRIMARY KEY, revision INTEGER NOT NULL, updated REAL NOT NULL, payload TEXT NOT NULL)")

    def create(self) -> dict:
        session_id = uuid4().hex
        state = {"comparison": None, "single_file": None, "metrics": [], "entity": None, "pending": None, "history": []}
        now = time.time()
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM agent_sessions WHERE updated < ?", (now - self.ttl_seconds,))
            self.connection.execute("INSERT INTO agent_sessions VALUES (?, 0, ?, ?)", (session_id, now, json.dumps(state)))
        return {"session_id": session_id, "revision": 0, "context": state}

    def get(self, session_id: str) -> dict:
        with self.lock:
            row = self.connection.execute("SELECT revision, updated, payload FROM agent_sessions WHERE id = ?", (session_id,)).fetchone()
        if row is None or row[1] < time.time() - self.ttl_seconds:
            raise SessionNotFoundError("Session was not found or has expired. Start a new chat without session_id.")
        return {"session_id": session_id, "revision": row[0], "context": json.loads(row[2])}

    def save(self, session: dict, state: dict) -> dict:
        now = time.time()
        with self.lock, self.connection:
            cursor = self.connection.execute(
                "UPDATE agent_sessions SET revision = revision + 1, updated = ?, payload = ? WHERE id = ? AND revision = ? AND updated >= ?",
                (now, json.dumps(state, allow_nan=False), session["session_id"], session["revision"], now - self.ttl_seconds),
            )
            if cursor.rowcount != 1:
                raise SessionConflictError("The session changed or expired during this request. Retry after the other request finishes.")
        return {"session_id": session["session_id"], "revision": session["revision"] + 1, "context": state}

    def delete(self, session_id: str):
        self.get(session_id)
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM agent_sessions WHERE id = ?", (session_id,))

    def close(self):
        with self.lock:
            self.connection.close()
