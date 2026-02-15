from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import SQLModel
from .api.auth_router import auth_router
from .api.task_router import task_router
from .chat.chat_routes import router as chat_router
from .chat.models import Conversation, Message  # Import chat models for database creation
from .config import settings
from .database.connection import engine

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Todo API", version="1.0.0")

# Create database tables
@app.on_event("startup")
def on_startup():
    from .models.user import User  # Import existing models to ensure they're registered
    from .models.task import Task  # Import existing models to ensure they're registered
    from .chat.models import Conversation, Message  # Import chat models to ensure they're registered
    SQLModel.metadata.create_all(bind=engine)

# Add rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(task_router, prefix="/todos", tags=["tasks"])
app.include_router(chat_router, tags=["chat"])  # No prefix since chat_router already has /api prefix



@app.get("/")
def read_root():
    return {"message": "Todo API - Phase III AI Chatbot Implementation"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Global exception handlers for consistent error responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_exception",
                "message": exc.detail if hasattr(exc, 'detail') else str(exc),
                "status_code": exc.status_code
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Validation error occurred",
                "details": exc.errors(),
                "status_code": 422
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_server_error",
                "message": "An unexpected error occurred",
                "status_code": 500
            }
        }
    )