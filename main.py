from src.scanner import CloudShieldScanner

scanner = CloudShieldScanner("data/sample_server.log", threshold=3)
report_path = scanner.scan()
print("Report saved to:", report_path)
