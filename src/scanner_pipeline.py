from src.reader import read_events
from collections import deque


class PipelineStage:
    """One stage in the scanner pipeline - a name, a function to run, and a link
    to the next stage."""

    def __init__(self, name: str, action):
        self.name = name
        self.action = action
        self.next = None

    def run(self, data):
        """Run this stage's action, then pass the result to the next stage."""
        print(f"-> running stage: {self.name}")
        result = self.action(data)
        if self.next is not None:
            return self.next.run(result)
        return result


def stage_read(log_path: str) -> list:
    """Stage 1: read all log lines using v1.1's generator reader."""
    return list(read_events(log_path, run_id="f8-pipeline"))


def stage_parse(log_events: list) -> list:
    """Stage 2: turn LogEvent dataclass objects into plain event dicts."""
    parsed = []
    for e in log_events:
        parsed.append(
            {
                "ip": e.ip,
                "event_time": e.timestamp,
                "event_type": e.method,
                "request": e.path,
                "status": e.status,
                "severity_score": None,
            }
        )
    return parsed


def stage_enrich(events: list) -> list:
    """Stage 3: give every event a real severity score, based on status code."""
    for event in events:
        event["severity_score"] = 8.0 if event["status"] in (401, 403) else 2.0
    return events


def stage_detect(events: list) -> list:
    """Stage 4: flag events with severity above 5 as suspicious."""
    for event in events:
        event["suspicious"] = event["severity_score"] > 5
    return events


def stage_store(events: list) -> int:
    """Stage 5: insert all events into the database, return count inserted."""
    from src.db import insert_events

    clean_events = [{k: v for k, v in e.items() if k != "suspicious"} for e in events]
    return insert_events(clean_events)


def build_scanner_pipeline():
    """Build and return the full read -> parse -> enrich -> detect -> store chain."""
    read = PipelineStage("read", stage_read)
    parse = PipelineStage("parse", stage_parse)
    enrich = PipelineStage("enrich", stage_enrich)
    detect = PipelineStage("detect", stage_detect)
    store = PipelineStage("store", stage_store)

    read.next = parse
    parse.next = enrich
    enrich.next = detect
    detect.next = store

    return read


def brackets_balanced(text: str) -> bool:
    """Check if all brackets in text are properly matched, using a stack."""
    stack: list = []
    pairs = {")": "(", "]": "[", "}": "{"}

    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False

    return len(stack) == 0


class AlertQueue:
    """A FIFO queue for alerts - processed in the order they arrived."""

    def __init__(self):
        self.items = deque()

    def enqueue(self, alert) -> None:
        """Add a new alert to the back of the queue."""
        self.items.append(alert)

    def dequeue(self):
        """Remove and return the oldest alert - the front of the queue."""
        if not self.items:
            return None
        return self.items.popleft()

    def __len__(self) -> int:
        return len(self.items)
