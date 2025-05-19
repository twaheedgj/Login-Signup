from fastapi import APIRouter, Depends, HTTPException
from services.user_services import UserService
from schemas.user import UserCreate, UserRead, UserProfileUpdate, UserPasswordUpdate
from services.auth_service import AuthService
from models.user import User
import uuid

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, user_service: UserService = Depends(UserService)):
    return user_service.create_user(user)

@router.get("/me", response_model=UserRead)
async def get_current_user(
    current_user: User = Depends(AuthService().get_current_user)
):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    current_user: User = Depends(AuthService().get_current_user),
    user_service: UserService = Depends(UserService)
):
    # Only allow users to get their own profile
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this user's data")
    return user_service.get_user(user_id)

@router.patch("/{user_id}/profile", response_model=UserRead)
async def update_profile(
    user_id: uuid.UUID,
    profile: UserProfileUpdate,
    current_user: User = Depends(AuthService().get_current_user),
    user_service: UserService = Depends(UserService)
):
    # Only allow users to update their own profile
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this user's data")
    return user_service.update_profile(user_id, profile)

@router.patch("/{user_id}/password", response_model=UserRead)
async def update_password(
    user_id: uuid.UUID,
    password_update: UserPasswordUpdate,
    current_user: User = Depends(AuthService().get_current_user),
    user_service: UserService = Depends(UserService)
):
    # Only allow users to update their own password
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this user's password")
    return user_service.update_password(user_id, password_update)

@router.delete("/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(AuthService().get_current_user),
    user_service: UserService = Depends(UserService)
):
    # Only allow users to delete their own account
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    return user_service.delete_user(user_id)
