from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse
from app.infra.database.config import engine
from app.infra.database.models import Base
from app.interfaces.http.controllers import router

# Cria tabelas (apenas para desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo API",
    description="API para gerenciamento de tarefas.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.include_router(router)

@app.get("/", response_class=PlainTextResponse)
async def root():
    return RedirectResponse(url="/docs")
    ##return "ToDo API está rodando! Acesse http://127.0.0.1:8000/docs para ver a documentação."