from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[float] #python > 3.10: datatype | None = None


class CreatePost(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: str
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Posts: Post
    Likes: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None


class Likes(BaseModel):
    post_id: int
    dir: conint(le=1)
