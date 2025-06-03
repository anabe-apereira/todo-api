from fastapi import FastAPI
from app.infra.database.config import engine
from app.infra.database.models import Base
from app.interfaces.http.controllers import router

# Cria tabelas (apenas para desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="API for managing tasks",
    version="1.0.0"
)

app.include_router(router)