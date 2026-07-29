import logging
import json
import sys
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)

def setup_logging(run_id: str = "") -> logging.Logger:
    logger = logging.getLogger("cloudshield")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = JsonFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("cloudshield.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger 

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"cloudshield.{name}")

def generate_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")   