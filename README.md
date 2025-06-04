# 📝 ToDo API - Gerenciamento de Tarefas

API RESTful para gerenciamento de tarefas, desenvolvida em **Python** com **FastAPI**, seguindo os princípios da Clean Architecture.

---

## 🚀 Funcionalidades

- ✅ CRUD completo de tarefas (`GET`, `POST`, `PUT`, `DELETE` em `/tasks`).
- ✅ Banco de dados relacional **SQLite**.
- ✅ Documentação interativa via **Swagger UI**.
- ✅ Testes unitários com **Pytest**.
- ✅ Containerização com **Docker**.

---

## 🛠️ Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [Pip](https://pip.pypa.io/)
- [Docker](https://www.docker.com/) (opcional, mas recomendado)
- [Git](https://git-scm.com/)

---

## 📦 Instalação Manual (Local)

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/todo-api.git
cd todo-api

### 2️⃣ Crie um ambiente virtual

python -m venv venv

Ativar no Windows:
venv\Scripts\activate

Ativar no Linux/Mac:
source venv/bin/activate

### 3️⃣ Instale as dependências
pip install -r requirements.txt

### 4️⃣ Execute o servidor
uvicorn app.interfaces.web.fastapi_app:app --reload

### 5️⃣ Acesse no navegador
Swagger UI 👉 http://127.0.0.1:8000/docs

###🐳 Executando com Docker

#### 1️⃣ Build da imagem
docker build -t todo-api .

#### 2️⃣ Rode o container
docker run -d --name todo-api -p 8000:8000 todo-api

#### 3️⃣ Acesse no navegador
Swagger UI 👉 http://localhost:8000/docs

#### 4️⃣ Parar o container
docker stop todo-api

##🧪 Executando os Testes
pytest --cov=app --cov-report=term-missing --cov-fail-under=80

##🔗 Endpoints Principais

| Método | Endpoint             | Descrição               |
| ------ | -------------------- | ----------------------- |
| GET    | `/api/v1/tasks`      | Listar todas as tarefas |
| POST   | `/api/v1/tasks`      | Criar nova tarefa       |
| GET    | `/api/v1/tasks/{id}` | Buscar tarefa por ID    |
| PUT    | `/api/v1/tasks/{id}` | Atualizar uma tarefa    |
| DELETE | `/api/v1/tasks/{id}` | Deletar uma tarefa      |

##💻 Arquitetura
O projeto segue os princípios da Clean Architecture, separado em:

domain — Entidades e contratos

usecases — Regras de negócio

infra — Banco de dados e repositórios

interfaces — Interface web (FastAPI)
