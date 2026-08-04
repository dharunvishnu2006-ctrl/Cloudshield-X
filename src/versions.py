import json
from pathlib import Path
from src.logging_setup import get_logger

logger = get_logger("versions")

VERSIONS_FILE = Path("docs/versions.json")


def load_versions(path: Path = VERSIONS_FILE) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"versions.json not found at {path}. " "Run from the project root."
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        versions = data.get("versions", [])
        logger.info(f"Loaded {len(versions)} versions")
        return versions
    except json.JSONDecodeError as e:
        raise ValueError(f"versions.json is malformed: {e}")


def current_version() -> dict:
    versions = load_versions()
    shipped = [v for v in versions if v["status"] == "shipped"]
    if not shipped:
        raise ValueError("No shipped versions found!")
    return shipped[-1]


def feature_lines(v: dict) -> list[str]:
    """Return each feature name as a display-ready bullet line."""
    return [f"- {name}" for name in v["features"]]


def bug_lines(v: dict) -> list[str]:
    """Return each fixed bug as a display-ready bullet line."""
    return [f"- {b}" for b in v["bugs_fixed"]]


def total_roadmap_steps(versions: list[dict]) -> int:
    """Return the highest step number across all version ranges."""
    ends = [int(v["steps"].split("-")[1]) for v in versions]
    return max(ends)
