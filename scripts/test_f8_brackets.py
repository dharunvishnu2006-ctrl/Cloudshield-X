import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.scanner_pipeline import brackets_balanced  # noqa: E402

print(brackets_balanced("{[}]"))
print(brackets_balanced("{[]}"))
print(brackets_balanced('{"key": [1, 2, 3]}'))
