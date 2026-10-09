"""Deterministic, conservative matching of user labels to real metric columns."""
from difflib import SequenceMatcher
import re
import unicodedata


DEFAULT_ALIASES = {"derivatives": "Derivatives PE"}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.sub(r"[\W_]+", " ", value).split())


class MetricMatchError(ValueError):
    def __init__(self, requested: str, candidates: list[str], ambiguous: bool = False):
        self.requested = requested
        self.candidates = candidates
        self.ambiguous = ambiguous
        message = f"Metric '{requested}' is ambiguous. Choose one of the candidates." if ambiguous else f"Unknown metric '{requested}'. Choose an available metric."
        super().__init__(message)


class MetricResolver:
    def __init__(self, aliases: dict[str, str] | None = None):
        self.aliases = {normalize(key): value for key, value in (DEFAULT_ALIASES if aliases is None else aliases).items()}

    def resolve(self, requested: str, available: list[str]) -> dict:
        label = normalize(requested)
        if not label:
            raise MetricMatchError(requested, available)
        if requested in available:
            return {"requested": requested, "resolved": requested, "method": "exact"}
        exact = [name for name in available if normalize(name) == label]
        if len(exact) == 1:
            return {"requested": requested, "resolved": exact[0], "method": "normalized"}
        if len(exact) > 1:
            raise MetricMatchError(requested, exact, True)
        target = self.aliases.get(label)
        if target:
            alias_matches = [name for name in available if normalize(name) == normalize(target)]
            if len(alias_matches) == 1:
                return {"requested": requested, "resolved": alias_matches[0], "method": "alias"}
            raise MetricMatchError(requested, alias_matches or available, len(alias_matches) > 1)
        partial = [name for name in available if f" {label} " in f" {normalize(name)} "]
        if len(partial) == 1:
            return {"requested": requested, "resolved": partial[0], "method": "partial"}
        if len(partial) > 1:
            raise MetricMatchError(requested, partial, True)
        scores = sorted(((SequenceMatcher(None, label, normalize(name)).ratio(), name) for name in available), reverse=True)
        if scores and scores[0][0] >= 0.80:
            nearby = [name for score, name in scores if score >= scores[0][0] - 0.10]
            if len(nearby) == 1:
                return {"requested": requested, "resolved": scores[0][1], "method": "fuzzy"}
            raise MetricMatchError(requested, nearby, True)
        raise MetricMatchError(requested, [name for _, name in scores[:5]])

    def resolve_many(self, requested: list[str] | None, available: list[str]) -> tuple[list[str], list[dict]]:
        if not requested:
            return list(available), []
        matches = [self.resolve(item, available) for item in requested]
        return list(dict.fromkeys(item["resolved"] for item in matches)), matches
