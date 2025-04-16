# Activate virtual environment
.\venv\Scripts\activate

# Set PYTHONPATH to include the functions directory
$env:PYTHONPATH = "$(Get-Location)\functions;$env:PYTHONPATH"

# Run tests
Write-Host "Running tests..."
pytest

# Start FastAPI application
Write-Host "Starting FastAPI application..."
cd functions
uvicorn app.main:app --reload --port 8000 