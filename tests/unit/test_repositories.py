import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.entities import Task
from app.infra.database.models import Base, TaskModel
from app.infra.database.repository import SQLiteTaskRepository

@pytest.fixture(scope="function")
def db_session():
    # Banco em memória isolado para cada teste
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Limpeza garantida
    session.rollback()
    session.close()

@pytest.fixture
def repo(db_session):
    return SQLiteTaskRepository(db_session)

@pytest.fixture
def sample_task(db_session):
    # Cria e retorna uma task de teste
    db_task = TaskModel(title="Test Task")
    db_session.add(db_task)
    db_session.commit()
    return db_task

def test_delete_task_success(repo, db_session, sample_task):
    # Testa a exclusão
    assert repo.delete(sample_task.id) is True
    
    # Verifica se foi realmente removido
    assert db_session.query(TaskModel).get(sample_task.id) is None

def test_list_all_tasks(repo, db_session, sample_task):
    tasks = repo.list_all()
    assert len(tasks) == 1
    assert tasks[0].id == sample_task.id