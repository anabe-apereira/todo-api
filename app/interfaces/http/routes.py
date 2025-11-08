"""
Classe para criar roteador principal, organiza rotas e mantém aplicação limpa e modular

"""

from fastapi import APIRouter
from app.interfaces.http.controllers import router as task_router

router = APIRouter()
router.include_router(task_router, prefix="/tasks", tags=["Tasks"])