from sqlalchemy.orm import Session

from app.api import deps


def test_get_db_deps():
    db = deps.get_db()
    session = next(db)
    assert isinstance(session, Session)
