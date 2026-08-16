FROM python:3.10-slim

WORKDIR /app

COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copia o código do Streamlit
COPY app.py ./

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar a interface
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]