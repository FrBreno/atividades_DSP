from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .category import PostCategory

class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None

class PostCategory(SQLModel, table=True):
    __tablename__ = "post_category"
    post_id: int = Field(default=None, foreign_key="post.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="category.id", primary_key=True)
class Category(CategoryBase, table=True):
    __tablename__ = "category"
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="categories", link_model=PostCategory)
