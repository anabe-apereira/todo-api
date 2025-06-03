from app.domain.entities import Task
from app.domain.repositories import TaskRepository

class TaskUseCases:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: Task) -> Task:
        # Validações de negócio (ex: título não pode ser vazio)
        if not task.title:
            raise ValueError("Title cannot be empty")
        return self.repository.create(task)

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def update_task(self, task_id: int, task: Task) -> Task | None:
        existing_task = self.repository.get_by_id(task_id)
        if not existing_task:
            return None
        return self.repository.update(task_id, task)

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)