FROM python:3.9-slim

WORKDIR /app

# 1. Копируем код сразу, чтобы bootstrap видел зависимости (если бы был requirements.txt)
COPY main.py .

# 2. Устанавливаем библиотеки приложения
RUN pip install fastapi uvicorn requests

# 3. Устанавливаем ядро OpenTelemetry
RUN pip install opentelemetry-distro opentelemetry-exporter-otlp

# 4. ВАЖНО: Эта команда докачивает плагины для FastAPI и Requests
RUN opentelemetry-bootstrap -a install

# Запуск
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
