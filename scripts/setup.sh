#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "Firebase CLI is not installed. Installing..."
    npm install -g firebase-tools
fi

# Check if Google Cloud SDK is installed
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK is not installed. Please install the Google Cloud SDK."
    exit 1
fi

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Initialize Firebase
echo "Initializing Firebase..."
firebase login
firebase use ridercritic

# Set up environment variables
echo "Setting up environment variables..."
cp .env.example .env
echo "Please update the .env file with your credentials."

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p model_cache
mkdir -p config

# Set up service account
echo "Setting up service account..."
if [ -f "config/firebase-credentials.json" ]; then
    echo "Firebase service account credentials found."
else
    echo "Please place your Firebase service account credentials in config/firebase-credentials.json"
fi

echo "Setup complete! Please follow these next steps:"
echo "1. Update the .env file with your credentials"
echo "2. Make sure config/firebase-credentials.json exists and contains valid credentials"
echo "3. Run 'firebase deploy' to deploy your project" 