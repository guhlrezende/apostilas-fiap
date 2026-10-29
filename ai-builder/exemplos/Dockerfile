# Imagem da API de triagem (apostila de AI Builder, cap. 4).
# Construir:  docker build -t triagem .
# Rodar:      docker run --rm -p 8000:8000 -e API_KEY=minha-chave triagem
FROM python:3.12-slim

WORKDIR /app

# Primeiro só as dependências: se o código mudar e elas não, o Docker reaproveita esta camada.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Depois o código.
COPY api.py .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
