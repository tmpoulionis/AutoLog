import re
from pathlib import Path

import autolog.config as config

_TS_RE = re.compile(r"###\s+\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\]")


def extract_timestamp(entry: str) -> str:
    """
    Return the ISO 8601 timestamp from a formatted entry string.
    """
    m = _TS_RE.search(entry)
    if not m:
        raise ValueError(f"No timestamp found in entry: {entry[:80]!r}")
    return m.group(1)


class LogStore:
    def __init__(self, project_name: str) -> None:
        self.project_dir = config.PROJECTS_DIR / project_name
        self.log_path    = self.project_dir / "log.md"
        self.media_dir   = self.project_dir / "media"

    def append(self, entry: str) -> None:
        """Append a formatted Markdown entry to log.md.

        Creates the project directory on first use. Always additive — no overwrite.
        """
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.media_dir.mkdir(parents=True, exist_ok=True)

        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(entry)
            if not entry.endswith("\n"):
                f.write("\n")

    def read_all_entries(self) -> list[str]:
        """Parse log.md and return a list of raw entry strings.

        Used by rebuild-index. Returns [] if log.md does not exist.
        """
        if not self.log_path.exists():
            return []

        raw = self.log_path.read_text(encoding="utf-8")
        chunks = [c.strip() for c in raw.split("\n---\n") if c.strip()]
        return [c for c in chunks if _TS_RE.search(c)]
