# tests/test_database.py
import os
import tempfile
from backend.database import Database

def test_db_create_and_user():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    path = tmp.name
    os.unlink(path)
    dbpath = path
    db = Database(dbpath)
    user = db.add_user("Test", "test@example.com", "pwd", role="student")
    assert user is not None
    fetched = db.get_user_by_email("test@example.com")
    assert fetched is not None
    assert fetched["name"] == "Test"
