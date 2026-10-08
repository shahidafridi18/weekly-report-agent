"""Small SQLite session records; selections/history persist, raw datasets do not."""
import json
from pathlib import Path
import sqlite3
from datetime import datetime, timezone
from threading import RLock
import time
from uuid import uuid4


class SessionNotFoundError(LookupError):
    pass


class SessionConflictError(RuntimeError):
    pass


class SessionStore:
    def __init__(self, path: str | Path = ":memory:", ttl_seconds: int = 30 * 86400):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(path), timeout=10, check_same_thread=False)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.lock = RLock()
        self.ttl_seconds = ttl_seconds
        with self.connection:
            self.connection.execute("CREATE TABLE IF NOT EXISTS agent_sessions (id TEXT PRIMARY KEY, revision INTEGER NOT NULL, updated REAL NOT NULL, payload TEXT NOT NULL)")
            self.connection.execute("""CREATE TABLE IF NOT EXISTS agent_turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
                message TEXT NOT NULL,
                answer TEXT NOT NULL,
                status TEXT NOT NULL,
                created REAL NOT NULL
            )""")
            self.connection.execute("CREATE INDEX IF NOT EXISTS agent_turns_session_id ON agent_turns(session_id, id)")

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
        return {"session_id": session_id, "revision": row[0], "updated_at": self._iso(row[1]),
                "updated_timestamp": row[1], "context": json.loads(row[2])}

    def save(self, session: dict, state: dict, turn: dict | None = None) -> dict:
        now = time.time()
        with self.lock, self.connection:
            cursor = self.connection.execute(
                "UPDATE agent_sessions SET revision = revision + 1, updated = ?, payload = ? WHERE id = ? AND revision = ? AND updated >= ?",
                (now, json.dumps(state, allow_nan=False), session["session_id"], session["revision"], now - self.ttl_seconds),
            )
            if cursor.rowcount != 1:
                raise SessionConflictError("The session changed or expired during this request. Retry after the other request finishes.")
            if turn is not None:
                # Existing databases kept only six context entries. Preserve those
                # available turns the first time an older session is continued.
                known = self.connection.execute(
                    "SELECT 1 FROM agent_turns WHERE session_id = ? LIMIT 1", (session["session_id"],)
                ).fetchone()
                if not known:
                    legacy = session["context"].get("history", [])
                    for item in legacy:
                        self.connection.execute(
                            "INSERT INTO agent_turns (session_id, message, answer, status, created) VALUES (?, ?, ?, ?, ?)",
                            (session["session_id"], item.get("message", ""), item.get("answer", ""), "legacy", session.get("updated_timestamp", now)),
                        )
                self.connection.execute(
                    "INSERT INTO agent_turns (session_id, message, answer, status, created) VALUES (?, ?, ?, ?, ?)",
                    (session["session_id"], turn["message"], turn["answer"], turn.get("status", "success"), now),
                )
        return {"session_id": session["session_id"], "revision": session["revision"] + 1, "context": state}

    @staticmethod
    def _iso(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    def get_turns(self, session_id: str) -> list[dict]:
        session = self.get(session_id)
        with self.lock:
            rows = self.connection.execute(
                "SELECT message, answer, status, created FROM agent_turns WHERE session_id = ? ORDER BY id", (session_id,)
            ).fetchall()
        if rows:
            return [{"message": message, "answer": answer, "status": status, "created_at": self._iso(created)}
                    for message, answer, status, created in rows]
        # Backward compatibility for sessions saved before transcript storage.
        return [{"message": item.get("message", ""), "answer": item.get("answer", ""),
                 "status": "legacy", "created_at": session["updated_at"]}
                for item in session["context"].get("history", [])]

    def list_sessions(self, limit: int = 100) -> dict:
        with self.lock:
            rows = self.connection.execute(
                "SELECT id, revision, updated, payload FROM agent_sessions WHERE updated >= ? ORDER BY updated DESC LIMIT ?",
                (time.time() - self.ttl_seconds, limit),
            ).fetchall()
        sessions = []
        for session_id, revision, updated, payload in rows:
            with self.lock:
                summary = self.connection.execute(
                    "SELECT message, answer FROM agent_turns WHERE session_id = ? ORDER BY id", (session_id,)
                ).fetchall()
            if not summary:
                summary = [(entry.get("message", ""), entry.get("answer", ""))
                           for entry in json.loads(payload).get("history", [])]
            if not summary:
                continue
            sessions.append({
                "session_id": session_id,
                "title": summary[0][0][:72] or "New conversation",
                "preview": summary[-1][1][:100],
                "updated_at": self._iso(updated),
                "turn_count": len(summary),
                "revision": revision,
            })
        return {"sessions": sessions, "count": len(sessions)}

    def delete(self, session_id: str):
        self.get(session_id)
        with self.lock, self.connection:
            self.connection.execute("DELETE FROM agent_sessions WHERE id = ?", (session_id,))

    def close(self):
        with self.lock:
            self.connection.close()
