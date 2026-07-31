def read_logs(filepath: str) -> list:
    """Read a server log file and return a list of dicts,
    one per line: {'time','ip','request','status'}."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()

        results = []
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            time = parts[0].strip()
            ip = parts[1].strip()
            request = parts[2].strip()
            status = parts[3].strip()
            log_dict = {"time": time, "ip": ip, "request": request, "status": status}
            results.append(log_dict)
        return results

    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        return []
