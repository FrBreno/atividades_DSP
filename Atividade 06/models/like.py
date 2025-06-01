from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .post import Post
    from .user import User

class Like(SQLModel, table=True):
    __tablename__ = "like"
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    post: Optional["Post"] = Relationship(back_populates="likes")
    user: Optional["User"] = Relationship(back_populates="likes")