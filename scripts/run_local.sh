#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Export environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests
echo "Running tests..."
pytest

# Start the application
echo "Starting FastAPI application..."
uvicorn app.main:app --reload --port 8000 