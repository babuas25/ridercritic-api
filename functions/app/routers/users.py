from app.config import Settings, get_settings
from app.dependencies import get_current_user_id
from app.models.user import UserResponse, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin import auth

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    try:
        user = auth.get_user(user_id)
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            photo_url=user.photo_url,
            email_verified=user.email_verified,
            disabled=user.disabled,
            roles=["user"],  # This should be fetched from your database
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate, user_id: str = Depends(get_current_user_id)
):
    try:
        update_data = {}
        if user_update.display_name is not None:
            update_data["display_name"] = user_update.display_name
        if user_update.photo_url is not None:
            update_data["photo_url"] = user_update.photo_url
        if user_update.email is not None:
            update_data["email"] = user_update.email

        user = auth.update_user(user_id, **update_data)
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            photo_url=user.photo_url,
            email_verified=user.email_verified,
            disabled=user.disabled,
            roles=["user"],  # This should be fetched from your database
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
