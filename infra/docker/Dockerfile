FROM python:3.12-slim

WORKDIR /app

# Dependências de sistema (mínimo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências primeiro (melhor cache)
COPY pyproject.toml uv.lock* /app/

# Instala uv e deps
RUN pip install --no-cache-dir uv \
 && uv sync --frozen || uv sync

# Copia o código
COPY . /app

EXPOSE 8000 8501

# Por padrão, sobe a API (você pode sobrescrever no compose)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
