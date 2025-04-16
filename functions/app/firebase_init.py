import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Get the path to the service account key file
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            # If not set in env, try to find it in the config directory
            cred_path = str(
                Path(__file__).parent.parent.parent
                / "config"
                / "firebase-credentials.json"
            )

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise
