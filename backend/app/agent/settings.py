from dataclasses import dataclass
import os
import json
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AgentSettings:
    input_directory: Path
    excel_directory: Path
    pdf_directory: Path
    session_database: Path | None = None
    metric_aliases: dict[str, str] | None = None

    def __post_init__(self):
        roots = [self.input_directory.resolve(), self.excel_directory.resolve(), self.pdf_directory.resolve()]
        for index, left in enumerate(roots):
            for right in roots[index + 1:]:
                if left.is_relative_to(right) or right.is_relative_to(left):
                    raise ValueError("Input, Excel report, and PDF report folders must be separate, non-nested folders.")

    @classmethod
    def from_env(cls):
        load_dotenv(BACKEND_DIRECTORY / ".env", override=False)

        def folder(name: str, default: str) -> Path:
            value = Path(os.getenv(name, default)).expanduser()
            return (value if value.is_absolute() else BACKEND_DIRECTORY / value).resolve()

        from app.agent.metric_resolver import DEFAULT_ALIASES
        aliases = dict(DEFAULT_ALIASES)
        custom = json.loads(os.getenv("METRIC_ALIASES_JSON", "{}"))
        if not isinstance(custom, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in custom.items()):
            raise ValueError("METRIC_ALIASES_JSON must be an object mapping text labels to column names.")
        aliases.update(custom)
        return cls(
            folder("WEEKLY_INPUT_DIR", "data/weekly"),
            folder("EXCEL_REPORT_DIR", "data/reports/excel"),
            folder("PDF_REPORT_DIR", "data/reports/pdf"),
            folder("AGENT_SESSION_DB", "data/agent_sessions.sqlite3"),
            aliases,
        )
