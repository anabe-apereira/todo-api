FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema para SQLite (opcional, mas recomendado)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cria diretório para o banco de dados SQLite
RUN mkdir -p /app/sqlite_db

# Permissões para o diretório (importante para Docker)
RUN chmod a+rwx /app/sqlite_db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]