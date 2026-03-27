from fastapi import FastAPI

app = FastAPI(title="Auto Profiling API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Auto Profiling API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
