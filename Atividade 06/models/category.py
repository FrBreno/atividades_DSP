from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="categories", link_model="PostCategory")

class PostCategory(SQLModel, table=True):
    post_id: int = Field(default=None, foreign_key="post.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="category.id", primary_key=True)