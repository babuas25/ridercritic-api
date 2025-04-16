from typing import Dict, Optional

from firebase_admin import auth
from firebase_admin.auth import UserRecord
from fastapi import HTTPException, status

class FirebaseAuthService:
    @staticmethod
    async def verify_token(token: str) -> Dict:
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
            )

    @staticmethod
    async def get_user(uid: str) -> UserRecord:
        try:
            return auth.get_user(uid)
        except auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {uid} not found",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @staticmethod
    async def create_user(email: str, password: str, display_name: Optional[str] = None) -> UserRecord:
        try:
            user_data = {
                "email": email,
                "password": password,
                "email_verified": False,
            }
            if display_name:
                user_data["display_name"] = display_name

            user = auth.create_user(**user_data)
            return user
        except auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @staticmethod
    async def update_user(uid: str, data: Dict) -> UserRecord:
        try:
            return auth.update_user(uid, **data)
        except auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {uid} not found",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @staticmethod
    async def delete_user(uid: str) -> None:
        try:
            auth.delete_user(uid)
        except auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {uid} not found",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @staticmethod
    async def create_custom_token(uid: str) -> str:
        try:
            return auth.create_custom_token(uid)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @staticmethod
    async def set_custom_claims(uid: str, claims: Dict) -> None:
        try:
            auth.set_custom_user_claims(uid, claims)
        except auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {uid} not found",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) 