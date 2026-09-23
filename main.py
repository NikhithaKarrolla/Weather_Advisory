from fastapi import FastAPI
from weather_routes import router

app = FastAPI(
    title="Weather Advisory API",
    description="Weather intelligence and agricultural advisory service",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Weather Advisory API is running",
        "status": "success"
    }