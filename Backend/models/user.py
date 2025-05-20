from sqlmodel import Field, SQLModel,Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4))
    first_name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    username: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True, nullable=False))
    email: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True, nullable=False))
    password: str = Field(exclude=True)
    is_verified: bool = Field(sa_column=Column(pg.BOOLEAN, default=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))