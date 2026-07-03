FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "src/scripts/sync_meta_ads.py"]
