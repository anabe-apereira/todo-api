from app.infra.database.config import engine, SessionLocal, create_tables

def test_engine_connection():
    conn = engine.connect()
    assert not conn.closed
    conn.close()

def test_session_factory():
    session = SessionLocal()
    assert session.bind == engine
    session.close()

def test_database_connection():
    # Testa se a engine foi criada corretamente
    assert engine is not None
    
    # Testa se consegue estabelecer uma sessão
    session = SessionLocal()
    assert session is not None
    session.close()

def test_create_tables():
    # Testa a criação de tabelas (em banco de memória)
    create_tables()
