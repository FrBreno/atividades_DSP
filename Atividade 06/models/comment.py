from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .post import Post
    from .user import User

class CommentBase(SQLModel):
    content: str

class Comment(CommentBase, table=True):
    __tablename__ = "comment"
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    post: Optional["Post"] = Relationship(back_populates="comments")
    user: Optional["User"] = Relationship(back_populates="comments")