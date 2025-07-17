# Base com Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . /app

# Instala bibliotecas do sistema necessárias para FAISS e PyPDF
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências do projeto
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Cria as pastas necessárias para documentos e FAISS
RUN mkdir -p documentos dsavectordb

# Define o comando padrão
CMD ["python", "main.py"]