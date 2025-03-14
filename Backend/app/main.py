from fastapi import FastAPI
from app.api.endpoints.employees import router as employees_router

app = FastAPI(title="TeamLink API")

app.include_router(employees_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to TeamLink API!"}
