import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.entities import Task
from app.infra.database.models import Base, TaskModel
from app.infra.database.repository import SQLiteTaskRepository

# 🔧 Configuração do banco em memória para os testes
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def repo(db_session):
    return SQLiteTaskRepository(db_session)

@pytest.fixture
def sample_task(db_session):
    db_task = TaskModel(title="Test Task")
    db_session.add(db_task)
    db_session.commit()
    return db_task

# ✅ Teste de criação
def test_create_task(repo, db_session):
    task = Task(title="New Task")
    result = repo.create(task)

    assert result.id is not None
    assert result.title == "New Task"
    assert result.completed is False

    # Verifica se persistiu no banco
    db_task = db_session.query(TaskModel).get(result.id)
    assert db_task is not None
    assert db_task.title == "New Task"

# ✅ Teste de busca por ID existente
def test_get_by_id_existing(repo, sample_task):
    result = repo.get_by_id(sample_task.id)
    assert result is not None
    assert result.id == sample_task.id
    assert result.title == "Test Task"

# ✅ Teste de busca por ID inexistente
def test_get_by_id_non_existing(repo):
    result = repo.get_by_id(999)
    assert result is None

# ✅ Teste de listagem
def test_list_all_tasks(repo, db_session, sample_task):
    tasks = repo.list_all()
    assert len(tasks) == 1
    assert tasks[0].id == sample_task.id

# ✅ Teste de atualização bem-sucedida
def test_update_task_success(repo, sample_task):
    updated_task = Task(
        id=sample_task.id,
        title="Updated Title",
        description="Updated description",
        completed=True
    )
    result = repo.update(sample_task.id, updated_task)

    assert result is not None
    assert result.title == "Updated Title"
    assert result.description == "Updated description"
    assert result.completed is True

# ✅ Teste de atualização com ID inexistente
def test_update_task_not_found(repo):
    updated_task = Task(
        id=999,
        title="Does Not Exist",
        description="Nothing",
        completed=False
    )
    result = repo.update(999, updated_task)
    assert result is None

# ✅ Teste de exclusão bem-sucedida
def test_delete_task_success(repo, db_session, sample_task):
    assert repo.delete(sample_task.id) is True
    assert db_session.query(TaskModel).get(sample_task.id) is None

# ✅ Teste de exclusão com ID inexistente
def test_delete_task_not_found(repo):
    assert repo.delete(999) is False
