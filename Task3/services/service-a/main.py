from fastapi import FastAPI
import requests
import os

app = FastAPI()
# Берем URL из переменных окружения, которые мы прописали в k8s/services.yaml
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8080")

@app.get("/")
def read_root():
    # Библиотеки opentelemetry автоматически подхватят этот вызов
    # и добавят заголовок traceparent (Distributed Tracing magic)
    try:
        response = requests.get(SERVICE_B_URL)
        return {
            "message": "Hello from Service A", 
            "service_b_response": response.json()
        }
    except Exception as e:
        return {"error": str(e)}
