import pytest
from app.domain.repositories import TaskRepository
from app.domain.entities import Task

def test_abstract_method_signatures():
    """Testa a implementação obrigatória dos métodos"""
    class TestRepo(TaskRepository):
        def create(self, task): return task
        def get_by_id(self, id): return None
        def update(self, id, task): return task
        def delete(self, id): return True
    
    repo = TestRepo()
    assert repo.create(Task(title="Teste")) is not None