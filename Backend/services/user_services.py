from core.database import get_session
from sqlmodel import Session
from fastapi import Depends, HTTPException
from models.user import User
from schemas.user import UserRead, UserProfileUpdate, UserPasswordUpdate
from schemas.auth import SignupRequest
from sqlalchemy import select
from datetime import datetime
from services.auth_service import AuthService
import uuid

class UserService:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db
        self.auth_service = AuthService(db)

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.db.exec(statement).first()
        return result[0] if result else None

    def create_user(self, user: SignupRequest) -> UserRead:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=self.auth_service.get_password_hash(user.password),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user(self, user_id: uuid.UUID) -> UserRead:
        statement = select(User).where(User.id == user_id)
        result = self.db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result[0]

    def update_profile(self, user_id: uuid.UUID, profile: UserProfileUpdate) -> UserRead:
        statement = select(User).where(User.id == user_id)
        result = self.db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        db_user = result[0]
        
        # Get only the fields that were explicitly set in the request
        update_data = profile.model_dump(exclude_unset=True, exclude_none=True)
        
        # Only update fields that were provided
        for field, value in update_data.items():
            if value is not None:  # Extra check to ensure we don't update with None values
                setattr(db_user, field, value)
        
        db_user.updated_at = datetime.now()
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_password(self, user_id: uuid.UUID, password_update: UserPasswordUpdate) -> UserRead:
        statement = select(User).where(User.id == user_id)
        result = self.db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        db_user = result[0]
        
        # Hash the new password
        db_user.password = self.auth_service.get_password_hash(password_update.password)
        db_user.updated_at = datetime.now()
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: uuid.UUID) -> dict:
        statement = select(User).where(User.id == user_id)
        result = self.db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        db_user = result[0]
        self.db.delete(db_user)
        self.db.commit()
        return {"message": "User deleted successfully", "status": "success", "user_id": str(user_id)}
