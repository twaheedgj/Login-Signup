from db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from schemas.user import UserCreateModel, UserModel
from models.user import User
from sqlmodel import select
from core.utils import hash_password
class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user: UserCreateModel) -> UserModel:
        user_data = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
        )
        user_data.password = hash_password(user.password)
        self.session.add(user_data)
        await self.session.commit()
        await self.session.refresh(user_data)
        return user_data
    
    async def get_user_by_email(self, email: str) -> UserModel:
        query = select(User).where(User.email == email)
        result = await self.session.exec(query)
        return result.first()
    
    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return user is not None
    
    async def update_user(self, user: User, user_data: dict) -> UserModel:
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    