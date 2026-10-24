from fastapi import FastAPI
from eir.routers.session import router as sessions_router
from eir.routers.patients import router as patients_router
from fastapi.middleware.cors import CORSMiddleware
from eir.core.config import settings
from eir.routers.auth import router as auth_router
app = FastAPI(
    title="EIR API",
    version="0.1.0",
    description="Pre consultation case-taking software",
)
app.include_router(sessions_router)
app.include_router(patients_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def root():
    return {"message": "App is running"}


app.include_router(auth_router)
@app.get('/health_status')
def health_status():
    return {"status": "healthy"}