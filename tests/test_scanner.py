import os
from src.log_reader import read_logs
from src.ip_detector import detect_suspicious_ips
from src.report_generator import generate_report


def test_read_logs_returns_list():
    result = read_logs("data/sample_server.log")
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert len(result[0]) == 4


def test_repeated_failures_flagged():
    logs = read_logs("data/sample_server.log")
    suspicious = detect_suspicious_ips(logs)
    assert "203.0.113.45" in suspicious


def test_clean_ip_not_flagged():
    logs = read_logs("data/sample_server.log")
    suspicious = detect_suspicious_ips(logs)
    assert "49.205.10.8" not in suspicious


def test_report_file_created():
    logs = read_logs("data/sample_server.log")
    suspicious = detect_suspicious_ips(logs)
    report_path = generate_report(suspicious)
    assert os.path.exists(report_path)


def test_missing_file_handled():
    result = read_logs("data/this_file_does_not_exist.log")
    assert result == []
