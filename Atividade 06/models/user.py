from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .comment import Comment
    from .like import Like

class UserBase(SQLModel):
    name: str
    email: str

class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)

    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="user")
    likes: List["Like"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    pass