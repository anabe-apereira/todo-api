from sqlalchemy.orm import Session
from app.domain.entities import Task
from app.infra.database.models import TaskModel

class SQLiteTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        # Convert input Task (Pydantic model) to dictionary
        task_data = task.model_dump() if hasattr(task, 'model_dump') else task.dict()
        
        # Create SQLAlchemy model instance
        db_task = TaskModel(**task_data)
        
        # Add to session and commit
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        # Convert SQLAlchemy model back to Pydantic model
        return Task.from_orm(db_task)

    def get_by_id(self, task_id: int) -> Task | None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return Task.from_orm()(db_task) if db_task else None

    def list_all(self) -> list[Task]:
        db_tasks = self.db.query(TaskModel).all()
        return [Task.from_orm(task) for task in db_tasks]

    def update(self, task_id: int, task: Task) -> Task | None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return None
        
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        return Task.from_orm(db_task)

    def delete(self, task_id: int) -> bool:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return False
        
        self.db.delete(db_task)
        self.db.commit()
        return True