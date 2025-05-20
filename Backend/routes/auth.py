from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_service import AuthService
from schemas.user import UserModel, UserCreateModel,UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from db.main import get_session
from core.utils import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from core.utils import generate_token
from core.config import Config
from fastapi.responses import JSONResponse
router = APIRouter()
@router.post("/register", response_model=UserModel)
async def register(user: UserCreateModel, session: AsyncSession = Depends(get_session), auth_service: AuthService = Depends(AuthService)):
    if await auth_service.user_exists(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return await auth_service.create_user(user)


@router.post("/login")
async def login_user(login_data:UserLoginModel, auth_service:AuthService = Depends(AuthService)):
    user = await auth_service.get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    access_token = generate_token(user_dict={"user_id":str(user.id),"email":user.email}, expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = generate_token(user_dict={"email":user.email,"user_id":str(user.id)}, expires_delta=timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS), refresh=True)
    return JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_verified": user.is_verified
        }
    }, status_code=status.HTTP_200_OK)
 