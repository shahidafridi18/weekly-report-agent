from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AgentSettings:
    input_directory: Path
    excel_directory: Path
    pdf_directory: Path

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

        return cls(
            folder("WEEKLY_INPUT_DIR", "data/weekly"),
            folder("EXCEL_REPORT_DIR", "data/reports/excel"),
            folder("PDF_REPORT_DIR", "data/reports/pdf"),
        )
