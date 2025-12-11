FROM python:3.13-slim

# Configurações gerais do Python e Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
  && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Copia manifestos primeiro (cache das dependências)
COPY pyproject.toml poetry.lock* ./

# Instala dependências principais
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Copia o código da aplicação
COPY core ./core
COPY utils ./utils
COPY middleware ./middleware
COPY main.py ./main.py
COPY logging.yaml ./logging.yaml
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini

# Permite imports absolutos simples
ENV PYTHONPATH="/app"

# Porta padrão reconhecida pelo Render
ENV PORT=8000

# Expor apenas a porta da aplicação
EXPOSE 8000

# Comando de inicialização compatível com ambiente de produção (Render define PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
