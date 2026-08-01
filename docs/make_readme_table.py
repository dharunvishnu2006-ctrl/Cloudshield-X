import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
VERSIONS_FILE = ROOT / "docs" / "versions.json"
README_FILE = ROOT / "README.md"

START_MARKER = "<!-- VERSIONS_TABLE_START -->"
END_MARKER = "<!-- VERSIONS_TABLE_END -->"


def load_versions() -> list[dict]:
    with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["versions"]


def make_table(versions: list[dict]) -> str:
    lines = []
    lines.append("| Version | Status | Steps | Tests | Description |")
    lines.append("|---------|--------|-------|-------|-------------|")
    for v in versions:
        status = "✅ Shipped" if v["status"] == "shipped" else "🔜 Planned"
        tests = str(v["tests"]) if v["tests"] > 0 else "—"
        lines.append(
            f"| **{v['version']}** | {status} | "
            f"{v['steps']} | {tests} | {v['description']} |"
        )
    return "\n".join(lines)


def update_readme(table: str) -> None:
    content = README_FILE.read_text(encoding="utf-8")
    if START_MARKER not in content:
        print("Markers not found in README.md — add them first!")
        return
    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]
    new_content = f"{before}{START_MARKER}\n{table}\n{END_MARKER}{after}"
    README_FILE.write_text(new_content, encoding="utf-8")
    print("README.md table updated!")


if __name__ == "__main__":
    versions = load_versions()
    table = make_table(versions)
    update_readme(table)
