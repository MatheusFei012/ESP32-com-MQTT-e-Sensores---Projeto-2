FROM python:3.10-slim

# Previne a criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Mantém a saída padrão do Python sem buffer para evitar situações em que
# o aplicativo falha sem emitir logs devido ao buffer. 
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Baixa e instala as dependências, aproveitando o cache do Docker
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copia o código fonte para o contêiner, exceto os arquivos listados no .dockerignore
COPY . .

# Executa o script
CMD python3 weather.py