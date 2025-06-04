import pytest
from sqlalchemy import text
from app.infra.database.config import engine, SessionLocal

def test_engine_creation():
    """Testa se a engine do SQLAlchemy foi criada corretamente"""
    assert engine is not None
    assert str(engine.url) == "sqlite:///./test.db"

def test_session_creation():
    """Testa se a sessão do banco de dados pode ser criada"""
    session = SessionLocal()
    assert session is not None
    
    # Testa uma consulta simples para verificar se a conexão funciona
    result = session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    
    session.close()

def test_session_autocommit_and_autoflush():
    """Testa se as configurações de autocommit e autoflush estão corretas"""
    session = SessionLocal()
    # Verifica as configurações do sessionmaker
    assert session.autoflush is False
    # A forma correta de verificar autocommit é através do sessionmaker
    assert session._autocommit is False  # Atributo interno
    session.close()