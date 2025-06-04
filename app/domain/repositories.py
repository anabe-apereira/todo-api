from abc import ABC, abstractmethod
from app.domain.entities import Task
from typing import List, Optional

class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass
    
    @abstractmethod
    def update(self, task_id: int, task: Task) -> Optional[Task]:
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass
    
    @abstractmethod
    def list_all(self) -> List[Task]:
        pass