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
- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)

---

## 📦 Instalação Manual (Local)

### 1️⃣ Clone o repositório

```bash
git https://github.com/anabe-apereira/todo-api
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

###🐳 Executando com Docker - Teste de Persistência

#### 1️⃣ Build da imagem
docker-compose up -d --build

#### 2️⃣ Verifica se o container está rodando
docker-compose ps

#### 3️⃣ Acesse no navegador
Swagger UI 👉 http://localhost:8000/docs

#### 4️⃣ Restartar o container
docker-compose restart

#### 5️⃣ Atualizar o Swagger + Consultar Alterações feitas
F5 na página do Swagger UI 

#### Pegar ID do docker
docker ps -a

#### 5️⃣ Parar o container
docker stop <container-id>

#### 6️⃣ Ligar o container novamente
docker-compose up 

#### 7️⃣ Atualizar o Swagger + Consultar Alterações feitas
F5 na página do Swagger UI 

#### 8️⃣ Encerrar o container e remover volumes (apaga dados e alterações)
docker-compose down

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
           — Interface http (Swagger UI )

##🗄️ Por que escolhi o SQLite?
Para este projeto, optei pelo uso do SQLite como banco de dados devido a alguns fatores estratégicos e técnicos que atendem bem à proposta da aplicação:

🔧 Familiaridade e Facilidade de Uso: Por ser um banco de dados relacional amplamente conhecido, o SQLite oferece uma curva de aprendizado muito baixa. Já possuo um bom domínio sobre seu funcionamento, o que facilita tanto o desenvolvimento quanto a manutenção da API.

⚙️ Simplicidade na Configuração: Diferente de outros bancos que exigem servidores ou serviços externos, o SQLite funciona baseado em arquivos locais, eliminando a necessidade de configuração de servidores de banco de dados. Isso agiliza a inicialização do ambiente e reduz complexidade.

📦 Portabilidade: O banco de dados é armazenado em um único arquivo (.db), o que permite transportar, versionar e compartilhar facilmente o projeto em diferentes ambientes de desenvolvimento.

🚀 Desempenho em Pequenas Aplicações: Apesar de ser leve, o SQLite é extremamente robusto para aplicações de pequeno e médio porte, além de ser capaz de lidar com múltiplas operações de leitura com eficiência.

🔒 Consistência e Confiabilidade: Como todo banco relacional, o SQLite oferece suporte completo a transações ACID (Atomicidade, Consistência, Isolamento e Durabilidade), garantindo integridade dos dados.

👨‍💻 Perfeito para Desenvolvimento e Testes: Para projetos locais, APIs de pequeno porte, protótipos ou MVPs, o SQLite se destaca por ser leve, estável e de fácil integração com frameworks como o FastAPI.

➡️ Posteriormente, caso haja necessidade de escalabilidade, a migração para bancos mais robustos, como PostgreSQL ou MySQL, pode ser feita com mínima refatoração, mantendo os princípios da arquitetura limpa adotada. 
