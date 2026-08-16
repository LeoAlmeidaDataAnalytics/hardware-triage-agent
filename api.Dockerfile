# Usa uma imagem oficial e leve do Python
FROM python:3.10-slim

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Copia o código da API e dos Agentes
COPY agent.py models.py multi_agent.py main.py ./

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a FastAPI
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]