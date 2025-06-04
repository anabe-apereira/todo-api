# app/interfaces/web/controllers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.domain.entities import Task
from app.infra.database.repository import SQLiteTaskRepository
from app.usecases.task_usecases import TaskUseCases
from app.infra.database.config import get_db

class TaskController:
    def __init__(self, router: APIRouter):
        self.router = router
        self._register_routes()

    def _register_routes(self):
        @self.router.post(
            "/tasks",
            response_model=Task,
            status_code=status.HTTP_201_CREATED,
            summary="Criação de nova tarefa",
            description="Cria uma nova tarefa com título, descrição e status de conclusão."
        )
        async def create_task(
            task: Task,
            usecases: TaskUseCases = Depends(self._get_usecases)
        ):
            try:
                return usecases.create_task(task)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "/tasks/{task_id}",
            response_model=Task,
            summary="Obter uma tarefa pelo ID",
            responses={
                404: {"description": "Task not found"}
            }
        )
        async def get_task(
            task_id: int,
            usecases: TaskUseCases = Depends(self._get_usecases)
        ):
            task = usecases.get_task_by_id(task_id)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return task

        @self.router.get(
            "/tasks",
            response_model=List[Task],
            summary="Listar todas as tarefas"
        )
        async def list_tasks(
            usecases: TaskUseCases = Depends(self._get_usecases)
        ):
            return usecases.list_tasks()

        @self.router.put(
            "/tasks/{task_id}",
            response_model=Task,
            summary="Atualizar uma tarefa",
            responses={
                404: {"description": "Task not found"}
            }
        )
        async def update_task(
            task_id: int,
            task: Task,
            usecases: TaskUseCases = Depends(self._get_usecases)
        ):
            updated_task = usecases.update_task(task_id, task)
            if not updated_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return updated_task

        @self.router.delete(
            "/tasks/{task_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Excluir uma tarefa",
            responses={
                404: {"description": "Task not found"}
            }
        )
        async def delete_task(
            task_id: int,
            usecases: TaskUseCases = Depends(self._get_usecases)
        ):
            if not usecases.delete_task(task_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            return None

    def _get_usecases(self, db: Session = Depends(get_db)):
        return TaskUseCases(SQLiteTaskRepository(db))


# Uso:
router = APIRouter(prefix="/api/v1", tags=["Tasks"])
TaskController(router)