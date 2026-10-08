from fastapi import FastAPI
import uvicorn
from src.eir.routers.session import router as sessions_router
from src.eir.routers.patients import router as patients_router
app = FastAPI(
    title="EIR API",
    version="0.1.0",
    description="Pre consultation case-taking software",
)
app.include_router(sessions_router)
app.include_router(patients_router)

@app.get('/')
def root():
    return {"message": "App is running"}

@app.get('/health_status')
def health_status():
    return {"status": "healthy"}