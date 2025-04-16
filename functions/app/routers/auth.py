from app.config import Settings, get_settings
from app.models.user import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from firebase_admin import auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, settings: Settings = Depends(get_settings)):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.display_name,
            photo_url=user.photo_url,
        )
        return UserResponse(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            email_verified=user_record.email_verified,
            disabled=user_record.disabled,
            roles=["user"],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = auth.get_user_by_email(form_data.username)
        # Verify password and create custom token
        custom_token = auth.create_custom_token(user.uid)
        return {"access_token": custom_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
