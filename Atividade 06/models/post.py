from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class PostBase(SQLModel):
    title: str
    content: str

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: Optional[str] = Field(default=None, nullable=True)
    updated_at: Optional[str] = Field(default=None, nullable=True)

    author: Optional["User"] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")
    likes: List["Like"] = Relationship(back_populates="post")
    categories: List["Category"] = Relationship(back_populates="posts", link_model="PostCategory")