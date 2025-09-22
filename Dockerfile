FROM python:3.12.9

WORKDIR /mcp/app
COPY . /mcp/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        curl \
        nano \
        tzdata && \
    # Install uv package manager
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    # limpar o cache do apt.
    rm -rf /var/lib/apt/lists/*

# Configura o fuso horário
RUN ln -snf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /mcp/app/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/mcp/app \
    MCP_LOG_LEVEL=INFO

# Default command
CMD ["python", "main.py", "--http"]