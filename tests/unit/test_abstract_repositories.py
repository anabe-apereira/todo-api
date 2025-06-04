import pytest
from app.domain.entities import Task
from app.domain.repositories import TaskRepository


# 🔧 Implementação concreta apenas para testes
class TestConcreteRepo(TaskRepository):
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def create(self, task: Task) -> Task:
        new_task = Task(
            id=self.next_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        self.tasks[self.next_id] = new_task
        self.next_id += 1
        return new_task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def update(self, task_id: int, task: Task) -> Task | None:
        if task_id not in self.tasks:
            return None
        updated_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        self.tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def list_all(self) -> list[Task]:
        return list(self.tasks.values())


# 🔥 Fixtures
@pytest.fixture
def repo():
    return TestConcreteRepo()


@pytest.fixture
def sample_task():
    return Task(title="Test Task", description="Test Description", completed=False)


# 🚥 Testes
def test_create_task(repo, sample_task):
    created = repo.create(sample_task)
    assert created.id == 1
    assert created.title == sample_task.title
    assert created.description == sample_task.description
    assert created.completed is False
    assert repo.get_by_id(1) == created


def test_get_by_id_found(repo, sample_task):
    created = repo.create(sample_task)
    found = repo.get_by_id(created.id)
    assert found == created


def test_get_by_id_not_found(repo):
    assert repo.get_by_id(999) is None


def test_update_task_success(repo, sample_task):
    created = repo.create(sample_task)
    updated_data = Task(title="Updated", description="Updated Desc", completed=True)
    updated = repo.update(created.id, updated_data)

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.description == "Updated Desc"
    assert updated.completed is True
    assert repo.get_by_id(created.id) == updated


def test_update_task_not_found(repo, sample_task):
    updated_data = Task(title="Updated", description="Updated Desc", completed=True)
    assert repo.update(999, updated_data) is None


def test_delete_task_success(repo, sample_task):
    created = repo.create(sample_task)
    assert repo.delete(created.id) is True
    assert repo.get_by_id(created.id) is None


def test_delete_task_not_found(repo):
    assert repo.delete(999) is False


def test_list_all_tasks(repo, sample_task):
    assert repo.list_all() == []

    task1 = repo.create(sample_task)
    task2 = repo.create(Task(title="Another", description="Desc", completed=True))

    tasks = repo.list_all()
    assert len(tasks) == 2
    assert task1 in tasks
    assert task2 in tasks


def test_abstract_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        TaskRepository()


def test_concrete_repo_implements_all_methods():
    repo = TestConcreteRepo()

    task = Task(title="Test", description="Desc", completed=False)

    created = repo.create(task)
    assert isinstance(created, Task)

    fetched = repo.get_by_id(created.id)
    assert isinstance(fetched, (Task, type(None)))

    updated = repo.update(created.id, Task(title="U", description="D", completed=True))
    assert isinstance(updated, (Task, type(None)))

    deleted = repo.delete(created.id)
    assert isinstance(deleted, bool)

    all_tasks = repo.list_all()
    assert isinstance(all_tasks, list)
    assert all(isinstance(t, Task) for t in all_tasks)
