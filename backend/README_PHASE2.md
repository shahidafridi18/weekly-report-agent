# Phase 2: conversational queries and metric matching

This update extends your existing FastAPI/Gemini agent. It remembers the selected
weekly files, metrics, and counterparty within a session, supports focused follow-up
questions, and resolves metric labels in Python. Calculations still use your existing
analysis engine. Excel and PDF reports retain the complete comparison.

## Apply the update

If you already applied Phase 1, extract this archive to a temporary folder, then
copy these items into your existing `backend/`:

- The complete `app/agent/` folder.
- `app/api/agent.py`.
- `test_agent_phase1.py` and `test_agent_phase2.py`.
- `README_PHASE2.md`, `README_PHASE1.md`, and `agent.env.example`.

Preserve your `.env`, actual input workbooks, and saved reports. Merge any local
customizations into the updated source. If Phase 1 is not yet installed, also apply
the source changes described in `README_PHASE1.md`, including the Matplotlib Agg
fix. The archive contains the full backend, but you do not need to replace files
that have not changed in Phase 2.

No new runtime packages are required. SQLite and the fuzzy matcher use the Python
standard library. Keep your existing Gemini key and working model configuration.
Optionally append this to `backend/.env` (it is also the default):

```dotenv
AGENT_SESSION_DB=data/agent_sessions.sqlite3
```

Run these commands from `backend/` in your existing virtual environment:

```bash
python -m unittest test_agent_phase1 test_agent_phase2 -v
python -m uvicorn app.main:app --reload
```

## Your comparison prompt

POST to `/api/agent/chat`:

```json
{
  "message": "Compare week 1 with week 3 for CVA Balance and derivatives"
}
```

Add your actual week 3 `.xlsx` workbook to `WEEKLY_INPUT_DIR` first. This archive
contains the two supplied week 1/week 2 samples only. A missing or ambiguous week
returns `needs_clarification` and available files; it does not substitute another week.

The response includes a `session_id`, the resolved file names, focused metric totals,
and `data.metric_name_matches`. For example, the matching audit for the label
`derivatives` is:

```json
{"requested": "derivatives", "resolved": "Derivatives PE", "method": "alias"}
```

## Metric matching

Matching ignores capitalization to accept the case variants in your examples. It
preserves the workbook's canonical column name in results. The same resolver is used
by chat and the direct analyze, compare, query, and report endpoints.

| Typed label | Result | Matching rule |
| --- | --- | --- |
| `Derivatives PE` | `Derivatives PE` | Exact column |
| `derivatives PE`, `DERIVATIVES PE` | `Derivatives PE` | Case normalization |
| `cva_balance` | `CVA Balance` | Case/spacing/punctuation normalization |
| `derivatives` | `Derivatives PE` | Explicit default alias |
| `derivates PE` | `Derivatives PE` | Simple spelling similarity |
| `balance` | `CVA Balance` | Unique phrase within a column name |
| `CE` | Ask: `Gross CE` or `Net CE` | Multiple matches |

The workbook schema contains other derivative-related metrics, so `derivatives`
is an explicit shortcut for `Derivatives PE`, rather than a generic partial match.
Other ambiguous labels require a choice. Unknown or low-confidence labels also
require clarification instead of selecting a guessed column.

The resolver checks exact names, normalized names, configured aliases, unique
whole-phrase partial matches, then `difflib.SequenceMatcher`. Fuzzy matches require
a similarity score of at least 0.80 and no other candidate within 0.10 of the top
score. This is a small spelling matcher, not semantic inference.

Add or override aliases in `.env`, then restart the backend:

```dotenv
METRIC_ALIASES_JSON={"cva":"CVA Balance","pe":"Derivatives PE"}
```

Aliases must target real metric columns. Exact or normalized real column names take
precedence over aliases. Send `metrics: []` to select all metrics; omitted chat metrics
reuse the current session's selection.

## Follow-ups

Start with an available pair:

```json
{"message": "Compare week 1 with week 2 for Gross CE"}
```

Copy the actual `session_id` returned by that request into each follow-up:

```json
{
  "session_id": "<returned session_id>",
  "message": "Which counterparties contributed most to that change?"
}
```

Other supported follow-up messages:

- `Show the three largest decreases for that metric.`
- `What changed for Counterparty 2?`
- `What about its Net CE?`
- `Which entities are new or removed?`
- `Which balances started from zero or dropped to zero?`
- `Now compare with week 3 for CVA Balance and derivatives PE.`
- `Generate both Excel and PDF reports for those weeks, including AI insights.`

Contributors include matched, new, and removed entities. Ranking uses absolute
numerical change; direction filters can select increases or decreases. The response
also includes the matched/new/removed movement bridge. Business causes that are not
present in the workbook cannot be inferred from these calculations.

Counterparties can be selected using a unique name, SIREN, Unique Identifier, or the
composite business-key label returned in results. Ambiguous selections return choices.
Single-file questions also work, such as `Summarize week 1 for Counterparty 2 and
Gross CE`, followed by `What about its Net CE?` with the same session ID.

For an exact single-week value, ask:

```json
{"message": "What is the Gross CE value for the week 2 report for UNIQUE IDENTIFIER 127?"}
```

The answer states `Gross CE = 561` for that entity in the supplied week 2 sample.
`data.metric_values` contains the selected row's actual cell values. A blank cell
is reported as missing, while a numeric zero is reported as zero. The word `report`
in a value question does not request creating a report.

The supplied week 1 sample does not contain Unique Identifier 127. Asking for that
identifier in week 1 returns `needs_clarification` with a not-found message naming
the workbook. It does not return a portfolio summary or use the week 2 value.
The selector has an explicit example for these lookups, and a narrow Python guard
preserves a single numeric SIREN/Unique Identifier mentioned in the current message
if the selector omits or misreads it. The guard also preserves explicitly named
schema metrics in that lookup. Other identifiers/names use the existing resolver.

This lookup fix changes `app/agent/orchestrator.py`, `app/agent/tools.py`, and
`test_agent_phase2.py` on top of Phase 2. Copy those updated files and restart the
server. If the answer still says "contains ... rows and ... columns; metric statistics
are in data.metric_statistics", check that the running server uses the updated
`app/agent/orchestrator.py`, rather than the Phase 1 generic reply.

After a clarification, send your choice with the same session ID. The pending
operation retains the requested files and other arguments. Omit `session_id` to
start an independent conversation. Different sessions do not share selections.

## Response and session behavior

Chat comparison/report responses are compact by default: selected metric totals,
row counts, movement bridges, matching audit, optional AI insights, and download
metadata. To retrieve the full original analysis through chat, set:

```json
{
  "message": "Compare week 1 with week 2 for Gross CE",
  "include_details": true
}
```

With that flag, `data.analysis` includes the complete analysis. The direct
`/api/agent/compare` and `/api/agent/reports` endpoints continue to return full analysis.
Any client that previously accessed `data.analysis` from chat should enable the flag
or use `data.metric_summary` for the focused totals.

Sessions persist in SQLite across backend restarts and expire after 24 hours of
inactivity. The records contain selections, source fingerprints, a pending operation,
and the six most recent short chat turns; raw worksheets and full analysis results
are not stored in the session. Requests reread the selected files and recalculate
results. If the bytes of a previously selected input change, the response reports
`source_changed_since_last_turn: true`. Send requests for one session sequentially;
conflicting concurrent updates return HTTP 409.

The additional session routes are:

| Method | Route | Purpose |
| --- | --- | --- |
| POST | `/api/agent/sessions` | Create an empty session |
| GET | `/api/agent/sessions/{session_id}` | Inspect its stored context |
| DELETE | `/api/agent/sessions/{session_id}` | Delete a session |

Unknown or expired IDs return HTTP 404; start a fresh chat without `session_id`.
Session IDs are context identifiers; application authentication remains your
deployment's responsibility.

## Deterministic queries without Gemini

POST `/api/agent/query` for focused queries independent of model selection:

```json
{
  "previous_file": "week 1",
  "current_file": "week 2",
  "metrics": ["gross ce"],
  "question": "contributors",
  "direction": "all",
  "limit": 5
}
```

`question` supports `metric_summary`, `contributors`, `entity`, `entities`, and
`zero_transitions`. An `entity` query also needs an `entity` label. `direction` applies
to contributors and supports `all`, `increase`, and `decrease`; `limit` is 1–20.
Contributor queries accept up to three selected metrics. These direct queries need
explicit file selectors, do not use session context, and do not generate AI insights.

Direct APIs return HTTP 409 for ambiguous metric/entity selections, HTTP 400 for an
unknown metric, and HTTP 404 for a missing workbook. Chat converts missing or
ambiguous selections into a normal `needs_clarification` response with a session ID.

## Verification and scope

The combined Phase 1/Phase 2 suite passed 58 tests using the supplied inputs and
the actual Excel reader, analysis engine, report generators, and FastAPI endpoints.
It checks matching, ambiguity, follow-ups, context isolation, SQLite persistence,
concurrent-update detection, changed input bytes, compact/full responses, and report
downloads. The week 3 selector test uses a temporary synthetic copy solely to test
file selection; no week 3 workbook is included or treated as actual data.

Gemini selection is mocked in the suite. Check the chat examples with your existing
API key/model after installation to validate live prompt-to-tool selection. Optional
insight failures still leave comparison and report generation available. The existing
Windows Matplotlib Agg fix is preserved. A TestClient `httpx` deprecation warning may
still appear independently of test success.

This phase uses your configured local input folder and separate Excel/PDF output
folders. SharePoint connectivity, unattended scheduling, and arbitrary multi-week
trend queries remain later integration work. The existing `FileSource` and
`ReportStore` interfaces provide the attachment points for a SharePoint source and
separate output destinations.

Official implementation references:

- https://docs.python.org/3/library/difflib.html
- https://docs.python.org/3/library/sqlite3.html
- https://ai.google.dev/api/generate-content
