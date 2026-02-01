FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN pip install fastapi uvicorn

RUN pip install opentelemetry-distro opentelemetry-exporter-otlp

# Магия здесь
RUN opentelemetry-bootstrap -a install

CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
