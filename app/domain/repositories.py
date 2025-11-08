"""
Classe abstrata que atua como um contrato que define operações obrigatórias sobre tarefas

"""
from abc import ABC, abstractmethod
from app.domain.entities import Task

class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task_id: int, task: Task) -> Task | None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass