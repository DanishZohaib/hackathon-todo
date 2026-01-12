from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth_router import auth_router
from .api.task_router import task_router
from .config import settings

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(task_router, prefix="/todos", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo API - Phase II Implementation"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}