from typing import Optional

from app.services.firebase_service import FirebaseAuthService
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class FirebaseAuthMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(FirebaseAuthMiddleware, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization credentials",
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        decoded_token = await FirebaseAuthService.verify_token(credentials.credentials)
        request.state.user = decoded_token
        return credentials


class AdminAuthMiddleware(FirebaseAuthMiddleware):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials = await super().__call__(request)

        if not request.state.user.get("admin", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        return credentials


# Create middleware instances
auth_required = FirebaseAuthMiddleware()
admin_required = AdminAuthMiddleware()
