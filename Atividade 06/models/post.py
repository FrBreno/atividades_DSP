from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

from .category import Category, PostCategory

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment
    from .like import Like

class PostBase(SQLModel):
    title: str
    content: str

class Post(PostBase, table=True):
    __tablename__ = "post"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    author: Optional["User"]    = Relationship(back_populates="posts")
    comments: List["Comment"]   = Relationship(back_populates="post")
    likes: List["Like"]         = Relationship(back_populates="post")
    categories: List["Category"]= Relationship(back_populates="posts", link_model=PostCategory)


class PostCreate(SQLModel):
    title: str
    content: str
    user_id: int
    category_ids: Optional[List[int]] = Field(default_factory=list)


class PostUpdate(SQLModel):
    title:  Optional[str] = None
    content: Optional[str] = None
    category_ids: Optional[List[int]] = Field(default_factory=list)
