from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routers (will be created in separate files)
# from .routers import disease, yield_pred, fertilizer, auth, users

# ML models will be loaded at startup
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup and cleanup on shutdown."""
    logger.info("Loading ML models...")
    try:
        from .ml_service import load_models
        global ml_models
        ml_models = load_models()
        logger.info(f"Successfully loaded {len(ml_models)} models")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
    
    yield
    
    # Cleanup
    logger.info("Shutting down...")
    ml_models.clear()

# Initialize FastAPI app
app = FastAPI(
    title="Tomato AI Guidance System API",
    description="Production-grade API for tomato disease detection, yield prediction, and fertilizer recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Tomato AI Guidance System",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "models_loaded": len(ml_models),
        "database": "connected"  # Will be implemented with DB
    }

# Include routers
from .routers import auth, disease, yield_pred

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(disease.router, prefix="/api/disease", tags=["Disease Detection"])
app.include_router(yield_pred.router, prefix="/api/yield", tags=["Yield Prediction"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
