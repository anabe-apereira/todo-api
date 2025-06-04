import pytest
from app.domain.entities import Task
from app.domain.repositories import TaskRepository

class TestConcreteRepo(TaskRepository):
    """Implementação concreta para testar a interface abstrata"""
    
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
    
    def create(self, task: Task) -> Task:
        """Cria uma nova task com ID incremental"""
        new_task = Task(
            id=self.next_id,
            title=task.title,
            description=task.description,
            completed=task.completed
        )
        self.tasks[self.next_id] = new_task
        self.next_id += 1
        return new_task
    
    def get_by_id(self, task_id: int) -> Task | None:
        """Busca task por ID ou retorna None"""
        return self.tasks.get(task_id)
    
    def update(self, task_id: int, task: Task) -> Task | None:
        """Atualiza task existente"""
        if task_id not in self.tasks:
            return None
        updated_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            completed=task.completed
        )
        self.tasks[task_id] = updated_task
        return updated_task
    
    def delete(self, task_id: int) -> bool:
        """Remove task e retorna se foi bem sucedido"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def list_all(self) -> list[Task]:
        """Retorna todas as tasks em uma lista"""
        return list(self.tasks.values())

@pytest.fixture
def repo():
    """Fixture que retorna uma instância do repositório de teste"""
    return TestConcreteRepo()

@pytest.fixture
def sample_task():
    """Fixture que retorna uma task de exemplo"""
    return Task(title="Test Task", description="Test Description")

def test_create_task(repo, sample_task):
    """Testa a criação de uma nova task"""
    created_task = repo.create(sample_task)
    
    assert created_task.id == 1
    assert created_task.title == sample_task.title
    assert created_task.description == sample_task.description
    assert repo.get_by_id(1) == created_task

def test_get_by_id_found(repo, sample_task):
    """Testa busca por ID quando a task existe"""
    created_task = repo.create(sample_task)
    found_task = repo.get_by_id(created_task.id)
    
    assert found_task == created_task

def test_get_by_id_not_found(repo):
    """Testa busca por ID quando a task não existe"""
    assert repo.get_by_id(999) is None

def test_update_task_success(repo, sample_task):
    """Testa atualização de task existente"""
    created_task = repo.create(sample_task)
    updated_data = Task(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )
    
    updated_task = repo.update(created_task.id, updated_data)
    
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is True
    assert repo.get_by_id(created_task.id) == updated_task

def test_update_task_not_found(repo, sample_task):
    """Testa atualização de task que não existe"""
    updated_data = Task(
        title="Updated Title",
        description="Updated Description"
    )
    
    assert repo.update(999, updated_data) is None

def test_delete_task_success(repo, sample_task):
    """Testa exclusão de task existente"""
    created_task = repo.create(sample_task)
    assert repo.delete(created_task.id) is True
    assert repo.get_by_id(created_task.id) is None

def test_delete_task_not_found(repo):
    """Testa exclusão de task que não existe"""
    assert repo.delete(999) is False

def test_list_all_tasks(repo, sample_task):
    """Testa listagem de todas as tasks"""
    # Lista vazia inicial
    assert repo.list_all() == []
    
    # Após adicionar tasks
    task1 = repo.create(sample_task)
    task2 = repo.create(Task(title="Another Task"))
    
    all_tasks = repo.list_all()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks

def test_abstract_repository_cannot_be_instantiated():
    """Testa que a classe abstrata não pode ser instanciada"""
    with pytest.raises(TypeError):
        TaskRepository()  # Deve falhar pois é abstrata

def test_concrete_repo_implements_all_methods():
    """Testa que a classe concreta implementa todos os métodos"""
    repo = TestConcreteRepo()
    
    # Verifica assinatura dos métodos
    task = Task(title="Test")
    assert isinstance(repo.create(task), Task)
    assert isinstance(repo.get_by_id(1), (Task, type(None)))
    assert isinstance(repo.update(1, task), (Task, type(None)))
    assert isinstance(repo.delete(1), bool)
    assert isinstance(repo.list_all(), list)
    assert all(isinstance(t, Task) for t in repo.list_all())