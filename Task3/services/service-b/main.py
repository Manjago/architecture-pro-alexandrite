from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def read_root():
    # Имитируем небольшую задержку для красоты трейса
    time.sleep(0.1) 
    return {"message": "Hello from Service B"}
