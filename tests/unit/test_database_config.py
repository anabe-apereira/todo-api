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
    # Testa a sessão criada pela fábrica de sessões
    db = SessionLocal()
    
    # Verifica as configurações padrão do SQLAlchemy 2.0+
    assert db.autocommit is False  # autocommit não existe mais como atributo direto
    assert db.autoflush is True  # Valor padrão recomendado
    
    # Verifica se é realmente uma sessão do SQLAlchemy
    assert isinstance(db, pytest.Session)
    
    # Testa o fechamento da sessão
    db.close()
    assert db.closed is True