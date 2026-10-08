import json
from pathlib import Path
import shutil
import sqlite3
from unittest import TestCase, main
from unittest.mock import Mock, patch

from app.agent.metric_resolver import MetricMatchError, MetricResolver
from app.agent.models import QueryRequest
from app.agent.orchestrator import GeminiToolSelector, WeeklyAgent
from app.agent.sessions import SessionConflictError, SessionNotFoundError, SessionStore
from app.schema import COUNTERPARTY_METRIC_COLUMNS
from app.ingestion.excel_reader import read_excel_bytes
import test_agent_phase1


class Phase2Tests(TestCase):
    # Reuse fixture setup, without rerunning the inherited Phase 1 test methods.
    setUp = test_agent_phase1.Phase1Tests.setUp

    def chat(self, action, arguments, message="Test request", session_id=None, include_details=False):
        self.selector.select.return_value = (action, arguments)
        body = {"message": message, "include_details": include_details}
        if session_id:
            body["session_id"] = session_id
        response = self.client.post("/api/agent/chat", json=body)
        self.assertEqual(response.status_code, 200, response.text[:1000])
        return response.json()

    def compare(self, metrics=None):
        args = {"previous_file": "week 1", "current_file": "week 2"}
        if metrics is not None:
            args["metrics"] = metrics
        return self.chat("compare_weekly_files", args)

    def test_case_and_punctuation_normalization(self):
        result = self.compare(["cva_balance", "derivatives pe"])
        self.assertEqual(list(result["data"]["metric_summary"]), ["CVA Balance", "Derivatives PE"])
        self.assertEqual([m["method"] for m in result["data"]["metric_name_matches"]], ["normalized", "normalized"])

    def test_requested_derivatives_alias_is_explicit_and_visible(self):
        result = self.compare(["derivatives"])
        self.assertEqual(result["data"]["metric_name_matches"], [{"requested": "derivatives", "resolved": "Derivatives PE", "method": "alias"}])
        self.assertEqual(list(result["data"]["metric_summary"]), ["Derivatives PE"])

    def test_simple_typo_and_unique_partial_match(self):
        result = self.compare(["derivates PE", "balance"])
        self.assertEqual(list(result["data"]["metric_summary"]), ["Derivatives PE", "CVA Balance"])
        self.assertEqual([m["method"] for m in result["data"]["metric_name_matches"]], ["fuzzy", "partial"])

    def test_ambiguous_partial_name_returns_candidates(self):
        result = self.compare(["ce"])
        self.assertEqual(result["status"], "needs_clarification")
        self.assertEqual(set(result["data"]["candidates"]), {"Gross CE", "Net CE"})
        self.assertIsNone(self.agent.sessions.get(result["session_id"])["context"]["comparison"])

    def test_metric_clarification_keeps_the_requested_pair(self):
        first = self.compare(["ce"])
        result = self.chat("compare_weekly_files", {"metrics": ["net ce"]}, "I meant Net CE", first["session_id"])
        self.assertEqual(result["status"], "success")
        self.assertEqual(list(result["data"]["metric_summary"]), ["Net CE"])
        self.assertIn("week1", result["data"]["comparison"]["previous_file"])

    def test_low_confidence_name_is_not_guessed(self):
        result = self.compare(["zzzyyxx"])
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("Unknown metric", result["answer"])

    def test_near_tie_fuzzy_candidates_require_clarification(self):
        with self.assertRaises(MetricMatchError) as caught:
            MetricResolver().resolve("alpha cst", ["Alpha Cost", "Alpha Cast"])
        self.assertTrue(caught.exception.ambiguous)

    def test_alias_target_must_exist_and_exact_names_win(self):
        resolver = MetricResolver({"derivatives": "Derivatives PE", "Net CE": "Gross CE"})
        with self.assertRaises(MetricMatchError):
            resolver.resolve("derivatives", ["Equity Derivatives"])
        self.assertEqual(resolver.resolve("Net CE", ["Net CE", "Gross CE"])["resolved"], "Net CE")

    def test_disabling_alias_exposes_real_derivative_ambiguity(self):
        with self.assertRaises(MetricMatchError) as caught:
            MetricResolver({}).resolve("derivatives", list(COUNTERPARTY_METRIC_COLUMNS))
        self.assertTrue(caught.exception.ambiguous)
        self.assertGreater(len(caught.exception.candidates), 1)

    def test_followup_reuses_files_and_metric_focus(self):
        first = self.compare(["gross ce"])
        result = self.chat("query_comparison", {"question": "contributors"}, "What drove that increase?", first["session_id"])
        self.assertEqual(result["session_id"], first["session_id"])
        self.assertEqual(list(result["data"]["contributors"]), ["Gross CE"])
        selected_context = self.selector.select.call_args.args[2]
        self.assertEqual(selected_context["metrics"], ["Gross CE"])
        self.assertIn("week1", selected_context["comparison"]["previous_file"])

    def test_contributors_include_new_and_removed_entities(self):
        result = self.tools.query_comparison(QueryRequest(previous_file="week 1", current_file="week 2", metrics=["gross ce"], question="contributors"))
        group = result["contributors"]["Gross CE"]
        top = group["top_contributors"]
        self.assertEqual(top[0]["entity"]["SIREN"], "SIREN 127")
        self.assertEqual(top[0]["status"], "new")
        self.assertEqual(top[0]["absolute_change"], 561)
        self.assertEqual(top[1]["absolute_change"], -368)
        self.assertEqual(group["movement_bridge"]["actual_total_change"], 254)
        stmp = self.tools.query_comparison(QueryRequest(previous_file="week 1", current_file="week 2", metrics=["total stmp"], question="contributors"))
        self.assertEqual(stmp["contributors"]["Total STMP"]["top_contributors"][0]["status"], "removed")

    def test_direction_and_limit_apply_to_python_results(self):
        result = self.client.post("/api/agent/query", json={"previous_file": "week 1", "current_file": "week 2", "metrics": ["gross ce"], "question": "contributors", "direction": "increase", "limit": 1})
        self.assertEqual(result.status_code, 200)
        rows = result.json()["contributors"]["Gross CE"]["top_contributors"]
        self.assertEqual(len(rows), 1)
        self.assertGreater(rows[0]["absolute_change"], 0)

    def test_followup_entity_name_and_metric_switch(self):
        first = self.compare(["gross ce"])
        entity = self.chat("query_comparison", {"question": "entity", "entity": "Counterparty 2"}, "What changed for Counterparty 2?", first["session_id"])
        self.assertEqual(entity["data"]["metric_changes"]["Gross CE"]["absolute_change"], -368)
        result = self.chat("query_comparison", {"question": "entity", "metrics": ["NET CE"]}, "What about its Net CE?", first["session_id"])
        self.assertEqual(result["data"]["entity"]["entity"]["SIREN"], "SIREN 2")
        self.assertEqual(result["data"]["metric_changes"]["Net CE"]["absolute_change"], -368)

    def test_new_and_removed_counterparty_names_can_be_looked_up(self):
        for name, expected in [("Counterparty 127", "new"), ("Counterparty 126", "removed")]:
            result = self.tools.query_comparison(QueryRequest(previous_file="week 1", current_file="week 2", metrics=["gross ce"], question="entity", entity=name))
            self.assertEqual(result["metric_changes"]["Gross CE"]["status"], expected)

    def test_ambiguous_entity_is_not_selected_silently(self):
        first = self.compare(["gross ce"])
        result = self.chat("query_comparison", {"question": "entity", "entity": "counterparty"}, session_id=first["session_id"])
        self.assertEqual(result["status"], "needs_clarification")
        self.assertGreater(len(result["data"]["candidates"]), 1)

    def test_new_removed_and_zero_transition_queries(self):
        first = self.compare(["gross ce"])
        entities = self.chat("query_comparison", {"question": "entities"}, session_id=first["session_id"])
        self.assertEqual(entities["data"]["new_entities"][0]["entity"]["SIREN"], "SIREN 127")
        zeros = self.chat("query_comparison", {"question": "zero_transitions"}, session_id=first["session_id"])
        self.assertEqual(zeros["data"]["matching_transitions"], 2)

    def test_no_context_does_not_reuse_another_session(self):
        first = self.compare(["gross ce"])
        second = self.chat("query_comparison", {"question": "contributors"})
        self.assertNotEqual(first["session_id"], second["session_id"])
        self.assertEqual(second["status"], "needs_clarification")

    def test_switching_pair_preserves_baseline_and_updates_current_file(self):
        # Synthetic test fixture only: rename a copy to exercise selector/context changes.
        shutil.copyfile(self.input / "counterparty_week2_formatted.xlsx", self.input / "fixture_week3.xlsx")
        first = self.compare(["cva balance", "derivatives"])
        result = self.chat("compare_weekly_files", {"current_file": "week 3", "metrics": ["CVA Balance", "derivates PE"]}, session_id=first["session_id"])
        self.assertIn("week1", result["data"]["comparison"]["previous_file"])
        self.assertEqual(result["data"]["comparison"]["current_file"], "fixture_week3.xlsx")
        self.assertEqual(list(result["data"]["metric_summary"]), ["CVA Balance", "Derivatives PE"])

    def test_missing_week3_does_not_fall_back_to_week2(self):
        result = self.chat("compare_weekly_files", {"previous_file": "week 1", "current_file": "week 3", "metrics": ["cva balance", "derivatives"]})
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("week 3", result["answer"])

    def test_single_file_entity_followups(self):
        first = self.chat("analyze_weekly_file", {"file": "week 1", "metrics": ["gross ce"], "entity": "SIREN 2"})
        self.assertEqual(first["data"]["metric_statistics"]["Gross CE"]["total"], 368)
        second = self.chat("analyze_weekly_file", {"metrics": ["net ce"]}, session_id=first["session_id"])
        self.assertEqual(second["data"]["row_count"], 1)
        self.assertEqual(second["data"]["metric_statistics"]["Net CE"]["total"], 368)
        self.assertIsNone(self.agent.sessions.get(first["session_id"])["context"]["comparison"])

    def test_requested_week1_identifier127_is_not_replaced_with_a_workbook_summary(self):
        result = self.chat("analyze_weekly_file", {"file": "week 1"},
                           "What is the Gross CE value for the week 1 report for UNIQUE IDENTIFIER 127.")
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("was not found", result["answer"])
        self.assertIn("counterparty_week1_formatted.xlsx", result["answer"])
        self.assertNotIn("metric_statistics", result["data"])
        self.assertNotIn("561", result["answer"])

    def test_explicit_identifier_and_metric_override_incorrect_selector_arguments(self):
        result = self.chat("analyze_weekly_file", {"file": "week 2", "entity": "SIREN 2", "metrics": ["Net CE"]},
                           "What is the Gross CE value for week 2 for UNIQUE IDENTIFIER 127?")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["row_count"], 1)
        self.assertEqual(result["data"]["metric_values"], {"Gross CE": 561})
        self.assertEqual(result["data"]["entity"]["entity"]["Unique Identifier"], "Unique Identifier 127")
        self.assertIn("Gross CE = 561", result["answer"])
        self.assertNotIn("total", result["answer"])

    def test_existing_week1_entity_returns_exact_value_in_answer(self):
        result = self.chat("analyze_weekly_file", {"file": "week 1"},
                           "What is gross ce for week 1 for unique identifier: 2?")
        self.assertEqual(result["data"]["metric_values"], {"Gross CE": 368})
        self.assertIn("Gross CE = 368", result["answer"])

    def test_zero_entity_value_is_returned_as_zero(self):
        result = self.chat("analyze_weekly_file", {"file": "week 1"},
                           "What is Gross CE for week 1 for UNIQUE IDENTIFIER 125?")
        self.assertEqual(result["data"]["metric_values"], {"Gross CE": 0})
        self.assertIn("Gross CE = 0", result["answer"])

    def test_missing_entity_cell_is_not_reported_as_zero(self):
        frame = read_excel_bytes((self.input / "counterparty_week1_formatted.xlsx").read_bytes())
        frame.loc[frame["Unique Identifier"] == "Unique Identifier 2", "Gross CE"] = float("nan")
        with patch("app.agent.tools.read_excel_bytes", return_value=frame):
            result = self.chat("analyze_weekly_file", {"file": "week 1"},
                               "What is Gross CE for week 1 for UNIQUE IDENTIFIER 2?")
        self.assertEqual(result["data"]["metric_values"], {"Gross CE": None})
        self.assertIn("Gross CE = missing (blank cell)", result["answer"])

    def test_whole_workbook_summary_is_still_available(self):
        result = self.chat("analyze_weekly_file", {"file": "week 1", "metrics": ["Gross CE"]},
                           "Summarize week 1 for Gross CE")
        self.assertEqual(result["data"]["row_count"], 126)
        self.assertIsNone(result["data"]["metric_values"])
        self.assertIn("total", result["answer"])

    def test_default_chat_is_compact_and_details_are_opt_in(self):
        compact = self.compare(["gross ce"])
        self.assertNotIn("analysis", compact["data"])
        self.assertLess(len(json.dumps(compact)), 10000)
        full = self.chat("compare_weekly_files", {"previous_file": "week 1", "current_file": "week 2"}, include_details=True)
        self.assertIn("variance_data", full["data"]["analysis"])

    def test_reports_reuse_session_and_return_compact_download_metadata(self):
        first = self.compare(["derivatives"])
        report = self.chat("generate_weekly_reports", {"report_format": "xlsx"}, "Generate an Excel report for those files", first["session_id"])
        self.assertEqual(len(report["data"]["reports"]), 1)
        self.assertNotIn("analysis", report["data"])
        artifact = report["data"]["reports"][0]
        downloaded = self.client.get(artifact["download_url"])
        self.assertEqual(downloaded.status_code, 200)
        self.assertIn(artifact["filename"], downloaded.headers["content-disposition"])

    def test_list_sessions_and_restore_transcript_through_api(self):
        first = self.compare(["gross ce"])
        self.chat("query_comparison", {"question": "contributors"}, "Who drove that change?", first["session_id"])
        listing = self.client.get("/api/agent/sessions")
        self.assertEqual(listing.status_code, 200)
        stored = next(item for item in listing.json()["sessions"] if item["session_id"] == first["session_id"])
        self.assertEqual(stored["turn_count"], 2)
        self.assertEqual(stored["title"], "Test request")
        details = self.client.get(f"/api/agent/sessions/{first['session_id']}")
        self.assertEqual(details.status_code, 200)
        self.assertEqual(len(details.json()["turns"]), 2)
        self.assertEqual(details.json()["turns"][1]["message"], "Who drove that change?")

    def test_metric_changes_in_followup_and_all_metrics_reset(self):
        first = self.compare(["cva balance"])
        second = self.chat("query_comparison", {"question": "metric_summary", "metrics": ["derivates PE"]}, session_id=first["session_id"])
        self.assertEqual(list(second["data"]["metric_summary"]), ["Derivatives PE"])
        all_metrics = self.chat("query_comparison", {"question": "metric_summary", "metrics": []}, session_id=first["session_id"])
        self.assertEqual(len(all_metrics["data"]["metric_summary"]), 24)

    def test_session_persists_across_store_restart(self):
        path = self.root / "sessions.sqlite3"
        store = SessionStore(path)
        agent = WeeklyAgent(self.tools, self.selector, store)
        self.selector.select.return_value = ("compare_weekly_files", {"previous_file": "week 1", "current_file": "week 2", "metrics": ["gross ce"]})
        first = agent.chat("Compare weeks")
        store.close()
        restarted = SessionStore(path)
        self.addCleanup(restarted.close)
        self.selector.select.return_value = ("query_comparison", {"question": "contributors"})
        second = WeeklyAgent(self.tools, self.selector, restarted).chat("What drove it?", first["session_id"])
        self.assertEqual(second["status"], "success")
        self.assertIn("Gross CE", second["data"]["contributors"])

    def test_unknown_expired_and_deleted_sessions(self):
        response = self.client.post("/api/agent/chat", json={"message": "Follow up", "session_id": "a" * 32})
        self.assertEqual(response.status_code, 404)
        session = self.agent.sessions.create()
        self.assertEqual(self.client.get("/api/agent/sessions/" + session["session_id"]).status_code, 200)
        self.assertEqual(self.client.delete("/api/agent/sessions/" + session["session_id"]).status_code, 200)
        with self.assertRaises(SessionNotFoundError):
            self.agent.sessions.get(session["session_id"])
        expired = SessionStore(ttl_seconds=-1)
        self.addCleanup(expired.close)
        with self.assertRaises(SessionNotFoundError):
            expired.get(expired.create()["session_id"])

    def test_concurrent_session_updates_are_detected(self):
        first = self.agent.sessions.create()
        stale = self.agent.sessions.get(first["session_id"])
        self.agent.sessions.save(first, first["context"])
        with self.assertRaises(SessionConflictError):
            self.agent.sessions.save(stale, stale["context"])

    def test_history_is_bounded_and_does_not_store_raw_analysis(self):
        first = self.compare(["gross ce"])
        for _ in range(8):
            self.chat("list_weekly_files", {}, session_id=first["session_id"])
        state = self.agent.sessions.get(first["session_id"])["context"]
        self.assertEqual(len(state["history"]), 6)
        self.assertNotIn("variance_data", json.dumps(state))

    def test_changed_input_bytes_are_reread_not_cached(self):
        first = self.compare(["gross ce"])
        current = self.input / "counterparty_week2_formatted.xlsx"
        shutil.copyfile(self.input / "counterparty_week1_formatted.xlsx", current)
        second = self.chat("query_comparison", {"question": "metric_summary"}, session_id=first["session_id"])
        self.assertTrue(second["data"]["source_changed_since_last_turn"])
        self.assertEqual(second["data"]["metric_summary"]["Gross CE"]["absolute_change"], 0)

    def test_sdk_receives_compact_context_without_raw_rows(self):
        llm = Mock()
        llm.model = "configured-model"
        llm.client.models.generate_content.return_value = Mock(function_calls=[Mock(name="query_comparison", args={"question": "contributors"})])
        llm.client.models.generate_content.return_value.function_calls[0].name = "query_comparison"
        with patch("app.insights.llm_service.GeminiService", return_value=llm):
            selected = GeminiToolSelector().select("What drove it?", self.source.list_files(), {"metrics": ["Gross CE"]})
        self.assertEqual(selected[0], "query_comparison")
        prompt = json.loads(llm.client.models.generate_content.call_args.kwargs["contents"])
        self.assertEqual(prompt["session_context"]["metrics"], ["Gross CE"])
        self.assertNotIn("variance_data", prompt)


if __name__ == "__main__":
    main()
