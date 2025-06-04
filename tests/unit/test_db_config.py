from app.infra.database.config import engine, SessionLocal

def test_engine_connection():
    conn = engine.connect()
    assert not conn.closed
    conn.close()

def test_session_factory():
    session = SessionLocal()
    assert session.bind == engine
    session.close()