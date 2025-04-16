# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import os

import firebase_functions
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RiderCritic API",
    description="API for RiderCritic application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"app_name": "RiderCritic", "version": "1.0.0", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Firebase Functions HTTP trigger
@firebase_functions.http_fn.on_request()
def fastapi_app(
    req: firebase_functions.http_fn.Request,
) -> firebase_functions.http_fn.Response:
    # Convert Firebase request to FastAPI request
    scope = {
        "type": "http",
        "method": req.method,
        "path": req.path,
        "headers": dict(req.headers),
        "query_string": req.query_string.encode(),
        "client": (req.remote_addr, 0),
        "server": (req.host, 80),
    }

    # Create FastAPI request
    request = Request(scope=scope)
    request._body = req.get_data()

    # Get FastAPI response
    response = app(request)

    # Convert FastAPI response to Firebase response
    return firebase_functions.http_fn.Response(
        status_code=response.status_code,
        headers=dict(response.headers),
        body=response.body,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
