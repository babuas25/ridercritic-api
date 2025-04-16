# Deployment Guide

## Environment Setup

### Development Environment
- Local development environment for testing and debugging
- Uses `.env` file for configuration
- Accessible at `http://localhost:8000`

### Staging Environment
- Pre-production environment for testing
- Uses `.env.staging` file for configuration
- Accessible at `https://staging.ridercritic.com`
- Mirrors production environment but with test data

### Production Environment
- Live environment for end users
- Uses `.env.production` file for configuration
- Accessible at `https://ridercritic.com`
- Requires careful deployment procedures

## Deployment Process

### 1. Local Development
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start development server
uvicorn app.main:app --reload --port 8000
```

### 2. Staging Deployment
```bash
# Set environment to staging
export ENVIRONMENT=staging  # Linux/Mac
$env:ENVIRONMENT="staging"  # Windows

# Deploy to Firebase
firebase deploy --only functions,hosting --project ridercritic-staging
```

### 3. Production Deployment
```bash
# Set environment to production
export ENVIRONMENT=production  # Linux/Mac
$env:ENVIRONMENT="production"  # Windows

# Deploy to Firebase
firebase deploy --only functions,hosting --project ridercritic-prod
```

## Testing Strategy

### 1. Local Testing
- Run unit tests: `pytest`
- Run with coverage: `pytest --cov=app`
- Run specific test file: `pytest tests/test_auth.py`

### 2. Staging Testing
- Automated tests run on GitHub Actions
- Manual testing of new features
- Load testing with simulated traffic
- Security testing and vulnerability scanning

### 3. Production Testing
- Smoke tests after deployment
- Monitoring for errors and performance
- A/B testing for new features
- User acceptance testing

## Environment Variables

### Required Variables
- `APP_NAME`: Application name
- `VERSION`: Application version
- `DEBUG`: Debug mode (True/False)
- `ENVIRONMENT`: Current environment (development/staging/production)
- `FIREBASE_PROJECT_ID`: Firebase project ID
- `FIREBASE_API_KEY`: Firebase API key
- `FIREBASE_AUTH_DOMAIN`: Firebase authentication domain
- `FIREBASE_STORAGE_BUCKET`: Firebase storage bucket
- `ALLOWED_ORIGINS`: List of allowed CORS origins

## Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use secure methods to store production credentials
- Rotate API keys and secrets regularly

### 2. Firebase Rules
- Review and update security rules before deployment
- Test rules in staging environment
- Monitor for unauthorized access

### 3. API Security
- Implement rate limiting
- Use HTTPS for all endpoints
- Validate all input data
- Implement proper error handling

## Monitoring and Maintenance

### 1. Logging
- Use structured logging
- Monitor error rates
- Track performance metrics

### 2. Backup
- Regular database backups
- Test restore procedures
- Document backup schedule

### 3. Updates
- Regular dependency updates
- Security patch management
- Version control strategy

## Troubleshooting

### Common Issues
1. **Deployment Failures**
   - Check Firebase project permissions
   - Verify environment variables
   - Review deployment logs

2. **Authentication Issues**
   - Verify Firebase configuration
   - Check token validation
   - Review security rules

3. **Performance Issues**
   - Monitor response times
   - Check database queries
   - Review caching strategy

### Support
- Contact development team for issues
- Check documentation for solutions
- Review error logs for details 