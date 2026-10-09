from datetime import datetime, timezone
from pathlib import Path
import re

from app.sources.base import AmbiguousFileError


def week_hint(name: str) -> int | None:
    match = re.search(r"(?:^|[_\s-])(?:week|w)[_\s-]*0*(\d+)(?=[_\s.\-]|$)", name, re.I)
    return int(match.group(1)) if match else None


class LocalFileSource:
    def __init__(self, input_directory: Path, max_bytes: int = 25 * 1024 * 1024):
        self.root = input_directory.resolve()
        self.max_bytes = max_bytes

    def list_files(self) -> list[dict]:
        if not self.root.is_dir():
            raise FileNotFoundError("Configured weekly input folder does not exist.")
        files = []
        for path in sorted(self.root.rglob("*")):
            if (not path.is_file() or path.suffix.lower() != ".xlsx"
                    or path.name.startswith("~$") or "_report" in path.stem.casefold()):
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(self.root):
                continue
            stat = resolved.stat()
            files.append({
                "file_id": path.relative_to(self.root).as_posix(),
                "filename": path.name,
                "week_hint": week_hint(path.name),
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            })
        return files

    def _resolve(self, selector: str) -> tuple[dict, Path]:
        selector = selector.strip()
        if not selector:
            raise ValueError("A filename, file_id, or week selector is required.")
        candidate_path = Path(selector)
        if ".." in candidate_path.parts:
            raise ValueError("Paths must stay within the configured weekly input folder.")
        if candidate_path.is_absolute():
            candidate_path = candidate_path.resolve()
            if not candidate_path.is_relative_to(self.root):
                raise ValueError("Paths must stay within the configured weekly input folder.")
            selector = candidate_path.relative_to(self.root).as_posix()
        files = self.list_files()
        normalized = selector.replace("\\", "/").casefold()
        matches = [f for f in files if f["file_id"].casefold() == normalized]
        if not matches:
            matches = [f for f in files if f["filename"].casefold() == normalized]
        week = re.fullmatch(r"(?:week|w)[\s_-]*0*(\d+)", selector, re.I)
        if not matches and week:
            matches = [f for f in files if f["week_hint"] == int(week.group(1))]
        if not matches:
            raise FileNotFoundError(f"No weekly input matches '{selector}'.")
        if len(matches) != 1:
            raise AmbiguousFileError(selector, [f["file_id"] for f in matches])
        info = matches[0]
        path = (self.root / info["file_id"]).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Input file resolves outside the configured input folder.")
        return info, path

    def read_file(self, selector: str) -> tuple[dict, bytes]:
        info, path = self._resolve(selector)
        if info["size_bytes"] > self.max_bytes:
            raise ValueError("Input file exceeds the configured size limit.")
        with path.open("rb") as handle:
            content = handle.read(self.max_bytes + 1)
        if not content or len(content) > self.max_bytes:
            raise ValueError("Input file is empty or exceeds the configured size limit.")
        return info, content
