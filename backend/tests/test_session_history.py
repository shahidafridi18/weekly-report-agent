"""Regression checks for SQLite conversation history (standard library only)."""
import tempfile
import copy
import unittest
from pathlib import Path

from app.agent.sessions import SessionStore


class SessionHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "sessions.sqlite3"
        self.store = SessionStore(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_list_and_restore_complete_transcript(self):
        created = self.store.create()
        session_id = created["session_id"]
        for number in range(9):
            session = self.store.get(session_id)
            state = copy.deepcopy(session["context"])
            state["history"] = (state["history"] + [{"message": f"Question {number}", "answer": f"Answer {number}"}])[-6:]
            self.store.save(session, state, {"message": f"Question {number}", "answer": f"Answer {number}", "status": "success"})

        sessions = self.store.list_sessions()["sessions"]
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]["title"], "Question 0")
        self.assertEqual(sessions[0]["turn_count"], 9)
        self.assertEqual(len(self.store.get_turns(session_id)), 9)
        self.assertEqual(len(self.store.get(session_id)["context"]["history"]), 6)

        self.store.close()
        reopened = SessionStore(self.path)
        self.assertEqual(len(reopened.get_turns(session_id)), 9)
        reopened.close()
        self.store = SessionStore(self.path)

    def test_legacy_sessions_are_still_readable(self):
        created = self.store.create()
        session = self.store.get(created["session_id"])
        state = copy.deepcopy(session["context"])
        state["history"] = [{"message": "Old question", "answer": "Old answer"}]
        self.store.save(session, state)
        turns = self.store.get_turns(created["session_id"])
        self.assertEqual(turns[0]["message"], "Old question")

        self.store.save(self.store.get(created["session_id"]), state,
                        {"message": "New question", "answer": "New answer"})
        self.assertEqual([turn["message"] for turn in self.store.get_turns(created["session_id"])],
                         ["Old question", "New question"])

    def test_deletion_removes_session_and_its_turns(self):
        created = self.store.create()
        session = self.store.get(created["session_id"])
        self.store.save(session, session["context"], {"message": "Hello", "answer": "Hi"})
        self.store.delete(created["session_id"])
        self.assertEqual(self.store.list_sessions()["count"], 0)
        with self.store.lock:
            remaining = self.store.connection.execute("SELECT count(*) FROM agent_turns").fetchone()[0]
        self.assertEqual(remaining, 0)


if __name__ == "__main__":
    unittest.main()
