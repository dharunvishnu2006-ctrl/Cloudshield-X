import re
from src.logging_setup import get_logger

logger = get_logger("parser")

LOG_PATTERN = re.compile(
    r"(?P<ip>\S+)"
    r"\s+(?P<dash1>\S+)"
    r"\s+(?P<dash2>\S+)"
    r"\s+\[(?P<timestamp>[^\]]+)\]"
    r'\s+"(?P<request>[^"]+)"'
    r"\s+(?P<status>\d{3})"
    r"\s+(?P<size>\S+)"
    r'(?:\s+"(?P<user_agent>[^"]+)")?'
)


def parse_line(line: str, run_id: str = "") -> dict | None:
    line = line.strip()
    if not line:
        return None

    match = LOG_PATTERN.match(line)
    if not match:
        logger.error(f"Parse failed run_id={run_id} line={line[:80]}")
        return None

    return match.groupdict()
