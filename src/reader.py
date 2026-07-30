import gzip
from pathlib import Path
from src.models import LogEvent
from src.parser import parse_line
from src.logging_setup import get_logger, generate_run_id

logger = get_logger("reader")

def read_events(path: str, run_id: str = "") -> LogEvent:
    file_path = Path(path)

    if not file_path.exists():
        logger.error(f"File not found: {path} run_id={run_id}")
        return

    opener = gzip.open if file_path.suffix == ".gz" else open

    with opener(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line, run_id=run_id)
            if parsed is None:
                continue
            try:
                yield LogEvent(
                    ip=str(parsed.get("ip", "")),
                    timestamp=parsed.get("timestamp", ""),
                    method=parsed.get("request", "").split()[0]
                        if parsed.get("request") else "",
                    path=parsed.get("request", "").split()[1]
                        if parsed.get("request") else "",
                    status=int(parsed.get("status", 0)),
                    user_agent=parsed.get("user_agent", "")
                )
            except Exception as e:
                logger.error(f"Event build failed: {e} "
                             f"run_id={run_id}")
                continue

def scan_directory(directory: str,
                   run_id: str = "") -> LogEvent:
    log_dir = Path(directory)
    if not log_dir.exists():
        logger.error(f"Directory not found: {directory}")
        return

    pattern = "**/*.log"
    log_files = list(log_dir.glob(pattern))
    log_files += list(log_dir.glob("**/*.gz"))

    logger.info(f"Found {len(log_files)} log files "
                f"run_id={run_id}")

    for log_file in log_files:
        yield from read_events(str(log_file), run_id)            