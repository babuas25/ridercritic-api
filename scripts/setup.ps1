# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python 3.10 or higher."
    exit 1
}

# Check if Rust is installed
if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "Rust is not installed. Installing Rust..."
    # Download and run rustup-init
    $rustupUrl = "https://win.rustup.rs"
    $rustupPath = "$env:TEMP\rustup-init.exe"
    Invoke-WebRequest -Uri $rustupUrl -OutFile $rustupPath
    Start-Process -FilePath $rustupPath -ArgumentList "-y" -Wait
    Remove-Item $rustupPath
    Write-Host "Rust installation complete. Please restart your terminal and run this script again."
    exit 0
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\activate

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
cd functions
pip install -r requirements.txt
cd ..

# Set PYTHONPATH to include the functions directory
$env:PYTHONPATH = "$(Get-Location)\functions;$env:PYTHONPATH"

# Initialize Firebase
Write-Host "Initializing Firebase..."
firebase login
firebase use ridercritic

# Set up environment variables
Write-Host "Setting up environment variables..."
Copy-Item .env.example .env
Write-Host "Please update the .env file with your credentials."

# Create necessary directories
Write-Host "Creating necessary directories..."
New-Item -ItemType Directory -Force -Path model_cache
New-Item -ItemType Directory -Force -Path config

# Set up service account
Write-Host "Setting up service account..."
if (Test-Path "config/firebase-credentials.json") {
    Write-Host "Firebase service account credentials found."
} else {
    Write-Host "Please place your Firebase service account credentials in config/firebase-credentials.json"
}

Write-Host "Setup complete! You can now run the application using .\scripts\test_and_run.ps1"
Write-Host "Please follow these next steps:"
Write-Host "1. Update the .env file with your credentials"
Write-Host "2. Make sure config/firebase-credentials.json exists and contains valid credentials"
Write-Host "3. Run 'firebase deploy' to deploy your project" 