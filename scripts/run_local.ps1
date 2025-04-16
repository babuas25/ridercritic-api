# Activate virtual environment
.\venv\Scripts\activate

# Export environment variables
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"

# Run tests
Write-Host "Running tests..."
pytest

# Start the application
Write-Host "Starting FastAPI application..."
uvicorn app.main:app --reload --port 8000 