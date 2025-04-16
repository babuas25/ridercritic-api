# RiderCritic API Developer Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Architecture](#architecture)
4. [API Documentation](#api-documentation)
5. [Development Workflow](#development-workflow)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)

## Project Overview
RiderCritic is a comprehensive motorcycle review platform that uses AI to generate and analyze reviews in Bangla. The platform consists of a FastAPI backend, Firebase services, and AI model integration.

### Key Features
- User authentication and authorization
- Motorcycle data management
- Review generation and analysis
- AI-powered content creation
- Data scraping and import
- Advanced search capabilities

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+
- Firebase CLI
- Google Cloud SDK
- Git

### Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/babuas25/ridercritic-api.git
   cd ridercritic-api
   ```

2. Run the setup script:
   - For Unix/Linux/Mac:
     ```bash
     chmod +x scripts/setup.sh
     ./scripts/setup.sh
     ```
   - For Windows:
     ```powershell
     .\scripts\setup.ps1
     ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your credentials

### Firebase Configuration
The project uses the following Firebase services:
- Authentication
- Firestore Database
- Storage
- Hosting
- Cloud Functions

Configuration files:
- `firebase.json`: Main Firebase configuration
- `firestore.rules`: Database security rules
- `storage.rules`: Storage security rules
- `firestore.indexes.json`: Database indexes

### Service Account Setup
1. Place your Firebase service account key in `config/firebase-credentials.json`
2. Ensure the service account has the following roles:
   - Firebase Admin
   - Cloud Functions Admin
   - Service Account User
   - Storage Admin

## Architecture

### Tech Stack
- Backend Framework: FastAPI
- Database: Firebase Firestore
- Authentication: Firebase Auth
- File Storage: Firebase Storage
- AI Model: BanglaT5/BanglaBERT
- CI/CD: GitHub Actions

### Directory Structure
```
ridercritic-api/
├── config/
│   ├── firebase-credentials.json
│   └── google-cloud.json
├── functions/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   └── main.py
├── public/
├── scripts/
│   ├── setup.sh
│   └── setup.ps1
├── tests/
├── .env
├── .gitignore
├── firebase.json
├── requirements.txt
└── README.md
```

## API Documentation

### Base URL
```
https://api.ridercritic.com/v1
```

### Authentication
All API endpoints require authentication using Firebase Authentication. Include the ID token in the Authorization header:
```
Authorization: Bearer <firebase_id_token>
```

### Error Handling
The API uses standard HTTP status codes and returns errors in the following format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

## Development Workflow

### Branch Strategy
- `main`: Production branch
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release branches

### Code Style
- Follow PEP 8 for Python code
- Use type hints
- Document all functions and classes
- Write unit tests for new features

### Commit Messages
Follow the conventional commits specification:
```
type(scope): description

[optional body]

[optional footer]
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

### Test Environment
- Tests use Firebase Emulator Suite
- Separate test database
- Mocked external services

## Deployment

### Environments
- Development: `https://dev.ridercritic.com`
- Staging: `https://staging.ridercritic.com`
- Production: `https://api.ridercritic.com`

### Deployment Process
1. Push to `develop` triggers deployment to development
2. Create PR to `main` triggers deployment to staging
3. Merge to `main` triggers deployment to production

## Security

### Authentication
- Firebase Authentication for user management
- JWT tokens for API authentication
- Role-based access control

### Data Security
- Firestore security rules
- Storage security rules
- Environment variable encryption

### API Security
- Rate limiting
- Input validation
- CORS configuration
- Request size limits

## Troubleshooting

### Common Issues
1. Authentication Errors
   - Verify Firebase configuration
   - Check token expiration
   - Validate service account permissions

2. Deployment Issues
   - Check GitHub Actions logs
   - Verify environment variables
   - Check Firebase CLI version

3. Local Development
   - Clear Firebase emulator cache
   - Reset virtual environment
   - Update dependencies

### Support
- Create GitHub issues for bugs
- Use pull requests for features
- Contact maintainers for critical issues

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 