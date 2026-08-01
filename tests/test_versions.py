import pytest
from src.versions import load_versions
from src.versions import feature_lines, bug_lines


def test_versions_json_parses():
    versions = load_versions()
    assert len(versions) > 0
    required_keys = {"version", "status", "colour", "completion"}
    for v in versions:
        for key in required_keys:
            assert key in v, f"Missing key '{key}' in {v['version']}"


def test_every_shipped_version_has_numbers():
    versions = load_versions()
    shipped = [v for v in versions if v["status"] == "shipped"]
    for v in shipped:
        assert v["tests"] > 0, f"{v['version']} has no tests"
        assert v["steps_covered"] > 0, f"{v['version']} missing steps"


def test_planned_versions_exist():
    versions = load_versions()
    planned = [v for v in versions if v["status"] == "planned"]
    assert len(planned) >= 4


def test_missinf_file_raises_error(tmp_path):
    fake_path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_versions(fake_path)


def test_feature_lines_include_all_features():
    v = {"features": ["A", "B", "C"]}
    lines = feature_lines(v)
    assert all(name in "\n".join(lines) for name in v["features"])


def test_bug_lines_are_sentences_not_counts():
    v = {"bugs_fixed": ["Fixed X", "Fixed Y"]}
    lines = bug_lines(v)
    assert len(lines) == 2
    assert "Fixed X" in lines[0]
