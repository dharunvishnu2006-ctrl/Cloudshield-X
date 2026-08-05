import os
import pytest
from src.db import init_db, DB_PATH


@pytest.fixture(autouse=True)
def clean_database():
    """Wipe the database before every single test, so tests never see
    leftover data from each other."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
