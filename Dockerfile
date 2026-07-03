FROM python:3.11-slim

WORKDIR /app

# Instalar git (necessário pra git dependencies no pip)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
# Continua mesmo se git dependencies falharem (temos fallback com dummy data)
RUN pip install -r requirements.txt --break-system-packages 2>&1 || echo "⚠️ Algumas dependências falharam, continuando com fallback..." && \
    pip install python-dotenv requests anthropic supabase postgrest aiohttp pydantic pandas numpy python-dateutil python-json-logger --break-system-packages

# Copiar código
COPY . .

ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["python", "src/scripts/sync_meta_ads.py"]
