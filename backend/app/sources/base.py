from typing import Protocol


class FileSource(Protocol):
    """SharePoint can later implement the same byte-based interface."""

    def list_files(self) -> list[dict]: ...

    def read_file(self, selector: str) -> tuple[dict, bytes]: ...


class AmbiguousFileError(ValueError):
    def __init__(self, selector: str, candidates: list[str]):
        self.candidates = candidates
        super().__init__(f"'{selector}' matches several files. Choose an exact file_id.")
