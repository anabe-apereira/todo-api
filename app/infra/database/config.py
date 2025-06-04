from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use banco em memória para testes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Teste para este arquivo (tests/unit/test_config.py)
def test_database_connection():
    from app.infra.database.config import engine, SessionLocal
    assert engine is not None
    session = SessionLocal()
    assert session is not None
    session.close()