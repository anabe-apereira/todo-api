import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infra.database.config import Base, get_db
from app.interfaces.http.controllers import TaskController

pytestmark = pytest.mark.usefixtures("clear_tables")

# 🔗 Configuração do banco de dados de testes
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🏗️ Cria as tabelas no início dos testes
Base.metadata.create_all(bind=engine)


# 🚀 Cria app e router
app = FastAPI()
router = APIRouter(prefix="/api/v1", tags=["Tasks"])
TaskController(router)
app.include_router(router)


# 🔧 Override da dependência get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# 🔄 Fixture para limpar tabelas antes de cada teste
@pytest.fixture(autouse=True, scope="function")
def clear_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.mark.usefixtures("clear_tables")
# 🚥 Testes de criação
def test_create_task():
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data

@pytest.mark.usefixtures("clear_tables")
def test_create_task_invalid_title():
    response = client.post("/api/v1/tasks", json={"title": "   "})
    assert response.status_code == 422  # Erro de validação do Pydantic/FastAPI

@pytest.mark.usefixtures("clear_tables")
# 🔍 Testes de recuperação
def test_get_task_existing():
    create_resp = client.post("/api/v1/tasks", json={"title": "Get Task"})
    task_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Task"

@pytest.mark.usefixtures("clear_tables")
def test_get_task_not_found():
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404

@pytest.mark.usefixtures("clear_tables")
# 🔄 Testes de update
def test_update_task_success():
    create_resp = client.post("/api/v1/tasks", json={"title": "Old Title"})
    task_id = create_resp.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={
        "title": "New Title",
        "description": "Updated Description",
        "completed": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

@pytest.mark.usefixtures("clear_tables")
def test_update_task_not_found():
    response = client.put("/api/v1/tasks/999", json={
        "title": "Doesn't Matter",
        "description": "No Task",
        "completed": False
    })
    assert response.status_code == 404

@pytest.mark.usefixtures("clear_tables")
# ❌ Testes de delete
def test_delete_task_success():
    create_resp = client.post("/api/v1/tasks", json={"title": "To be deleted"})
    task_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204

    # Verifica que não existe mais
    get_resp = client.get(f"/api/v1/tasks/{task_id}")
    assert get_resp.status_code == 404

@pytest.mark.usefixtures("clear_tables")
def test_delete_task_not_found():
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
