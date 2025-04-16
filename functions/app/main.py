from app.config import Settings, get_settings
from app.firebase_init import initialize_firebase
from app.routers import auth, users
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize Firebase
initialize_firebase()

app = FastAPI(
    title="RiderCritic API",
    description="API for RiderCritic application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "environment": "development" if settings.debug else "production",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
