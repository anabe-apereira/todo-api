import pytest
from abc import ABC, abstractmethod
from app.domain.entities import Task
from app.domain.repositories import TaskRepository

# Classe de teste concreta que implementa todos os métodos abstratos
class TestConcreteRepo(TaskRepository):
    def create(self, task: Task) -> Task:
        return task
    
    def get_by_id(self, task_id: int) -> Task | None:
        return Task(id=task_id, title="Test")
    
    def update(self, task_id: int, task: Task) -> Task | None:
        return task
    
    def delete(self, task_id: int) -> bool:
        return True
    
    def list_all(self) -> list[Task]:
        return [Task(id=1, title="Test")]

def test_abstract_method_signatures():
    # Testa se podemos instanciar a classe concreta
    repo = TestConcreteRepo()
    
    # Testa cada assinatura de método
    task = Task(title="Test")
    assert isinstance(repo.create(task), Task)
    assert isinstance(repo.get_by_id(1), (Task, type(None)))
    assert isinstance(repo.update(1, task), (Task, type(None)))
    assert isinstance(repo.delete(1), bool)
    assert isinstance(repo.list_all(), list)
    assert all(isinstance(t, Task) for t in repo.list_all())