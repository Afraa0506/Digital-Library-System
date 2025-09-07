# tests/test_models.py
import tempfile, os
from backend.database import Database
from backend.models import LibrarySystem

def test_register_and_upload():
    tmpfile = tempfile.NamedTemporaryFile(delete=False).name
    os.unlink(tmpfile)
    db = Database(tmpfile)
    lib = LibrarySystem(db)
    u = lib.register_user("T", "t@example.com", "p", role="teacher")
    assert u is not None
    # upload without file should succeed
    rid = lib.upload_resource("Sample", "Author", "ebook", None, uploaded_by=u.user_id)
    assert rid is not None
    res = lib.search_resources("Sample")
    assert len(res) >= 1
