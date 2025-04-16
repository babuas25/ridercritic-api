from app.config import Settings, get_settings
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import initialize_app

# Initialize Firebase Admin
firebase_app = initialize_app()

# Create FastAPI app
app = FastAPI(
    title="RiderCritic API",
    description="A comprehensive motorcycle review platform API",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ridercritic.firebaseapp.com",
        "https://ridercritic.web.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.routes import auth, bikes, reviews, users

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(bikes.router, prefix="/api/v1/bikes", tags=["Bikes"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.app_name,
        "version": settings.version,
        "status": "running",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
