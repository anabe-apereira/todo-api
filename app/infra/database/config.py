import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuração base
Base = declarative_base()

# Verifica se está em modo de teste (pode ser definido via variável de ambiente)
TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")

if TESTING:
    # Configuração para testes - banco em memória
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Configuração para desenvolvimento/produção
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'sqlite_db', 'tasks.db')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para injetar a sessão do banco (usada em endpoints FastAPI/Flask)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar tabelas (útil para testes e inicialização)
def create_tables():
    Base.metadata.create_all(bind=engine)