from sqlalchemy.orm import Session
from app.domain.entities import Task
from app.infra.database.models import TaskModel

class SQLiteTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        task_data = task.model_dump()
        db_task = TaskModel(**task_data)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return Task.model_validate(db_task)

    def get_by_id(self, task_id: int) -> Task | None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return Task.model_validate(db_task) if db_task else None

    def list_all(self) -> list[Task]:
        db_tasks = self.db.query(TaskModel).all()
        return [Task.model_validate(task) for task in db_tasks]

    def update(self, task_id: int, task: Task) -> Task | None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return None

        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)
        return Task.model_validate(db_task)

    def delete(self, task_id: int) -> bool:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True
