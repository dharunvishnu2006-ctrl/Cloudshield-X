from src.log_reader import read_logs
from src.ip_detector import detect_suspicious_ips
from src.alert_system import raise_alerts
from src.report_generator import generate_report


class CloudShieldScanner:
    def __init__(self, filepath, threshold=3):
        self.filepath = filepath
        self.threshold = threshold

    def scan(self):
        logs = read_logs(self.filepath)
        suspicious = detect_suspicious_ips(logs, self.threshold)
        raise_alerts(suspicious)
        report_path = generate_report(suspicious)
        return report_path
