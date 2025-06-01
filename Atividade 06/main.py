from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlmodel import select, func
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import create_db_and_tables, get_session
from core.loggingConfig import setup_logging

from models.user import User, UserCreate
from models.category import Category, PostCategory
from models.post import Post, PostCreate, PostUpdate
from models.comment import Comment
from models.like import Like

app = FastAPI()

setup_logging()
# TODO: Chamar apenas quando não há as tabelas criadas
create_db_and_tables()

# Crud Routes

## Users 
user_router = SQLAlchemyCRUDRouter(
    db_model=User,
    schema=User,
    create_schema=UserCreate,
    prefix='/users',
    tags=['Users'],
    db=get_session
)
app.include_router(user_router)

@app.post("/posts", response_model=Post, tags=["Posts"])
def create_post(post_in: PostCreate, session: Session = Depends(get_session)):
    # 1. Cria o Post "base"
    new_post = Post(
        title=post_in.title,
        content=post_in.content,
        user_id=post_in.user_id
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    # 2. Para cada category_id enviado, cria registro em post_category
    for cat_id in post_in.category_ids or []:
        # Opcional: verificar se a categoria existe
        try:
            session.exec(select(Category).where(Category.id == cat_id)).one()
        except:
            raise HTTPException(status_code=404, detail=f"Categoria {cat_id} não encontrada.")
        link = PostCategory(post_id=new_post.id, category_id=cat_id)
        session.add(link)

    session.commit()
    session.refresh(new_post)
    return new_post




## Categorys
category_router = SQLAlchemyCRUDRouter(
    db_model=Category,
    schema=Category,
    prefix="/category",
    tags=["Category"],
    db=get_session
)
app.include_router(category_router)

## Posts
post_router = SQLAlchemyCRUDRouter(
    db_model=Post,
    schema=Post,
    create_schema=PostCreate,
    update_schema=PostUpdate,
    prefix="/posts",
    tags=["Posts"],
    db=get_session
)
app.include_router(post_router)

## Comments
comment_router = SQLAlchemyCRUDRouter(
    db_model=Comment,
    schema=Comment,
    prefix="/comments",
    tags=["Comments"],
    db=get_session
)
app.include_router(comment_router)

## Likes
like_router = SQLAlchemyCRUDRouter(
    db_model=Like,
    schema=Like,
    prefix="/likes",
    tags=["Likes"],
    db=get_session
)
app.include_router(like_router)

# Paginated Routers

## Users
@app.get("/users-pagination", tags=["Users"])
def get_users_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=10, le=100, description="Quantidade de resultados por página (Por padrão é 10 e seu limite é 100)"),
    session: Session = Depends(get_session)
):
    total_records = session.exec(select(func.count(User.id))).one()
    total_pages = (total_records + page_size - 1)
    offset = (page -1 ) * page_size

    query = select(User).offset(offset).limit(page_size)
    results: List[User] = session.exec(query).all()

    return {
        "data": results,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }

## Categorys
@app.get("/category-pagination", tags=["Category"])
def get_categorias_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=10, le=100, description="Quantidade de resultados por página (Por padrão é 10 e seu limite é 100)"),
    session: Session = Depends(get_session)
):
    total_records = session.exec(select(func.count(Category.id))).one()
    total_pages = (total_records + page_size - 1)
    offset = (page -1 ) * page_size

    query = select(Category).offset(offset).limit(page_size)
    results: List[Category] = session.exec(query).all()

    return {
        "data": results,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }

@app.get("/category-pagination/stats", tags=["Category"])
def get_category_stats(
    session: Session = Depends(get_session)
):
    stmt = (
        select(
            Category.id.label("id"),
            Category.name.label("name"),
            func.count(PostCategory.post_id).label("total_posts")
        )
        .outerjoin(PostCategory, Category.id == PostCategory.category_id)
        .group_by(Category.id)
        .order_by(func.count(PostCategory.post_id).desc())
    )

    resultados = session.exec(stmt).all()

    return [
        {"id": row.id, "name": row.name, "total_posts": row.total_posts}
        for row in resultados
    ]

## Posts
@app.get("/posts-pagination", tags=["Posts"])
def get_posts_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=1, le=100, description="Quantidade de resultados por página (padrão 10, máximo 100)"),
    search: Optional[str] = Query(None, description="Buscar palavra-chave em title ou content"),
    category_id: Optional[int] = Query(None, description="Filtrar por ID de categoria"),
    session: Session = Depends(get_session)
):
    stmt = select(Post).distinct(Post.id)

    if category_id is not None:
        stmt = stmt.join(
            PostCategory,
            Post.id == PostCategory.post_id
        ).where(
            PostCategory.category_id == category_id
        )

    if search:
        ilike_pattern = f"%{search}%"
        stmt = stmt.where(
            (Post.title.ilike(ilike_pattern)) |
            (Post.content.ilike(ilike_pattern))
        )

    count_stmt = select(func.count(func.distinct(Post.id)))

    if category_id is not None:
        count_stmt = count_stmt.join(
            PostCategory,
            Post.id == PostCategory.post_id
        ).where(
            PostCategory.category_id == category_id
        )

    if search:
        ilike_pattern = f"%{search}%"
        count_stmt = count_stmt.where(
            (Post.title.ilike(ilike_pattern)) |
            (Post.content.ilike(ilike_pattern))
        )

    total_records = session.exec(count_stmt).one()
    total_pages = (total_records + page_size - 1) // page_size

    if page > total_pages and total_records > 0:
        raise HTTPException(status_code=404, detail="Página não encontrada")

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    posts: List[Post] = session.exec(stmt).all()

    data = []
    for post in posts:
        category_ids = [cat.id for cat in post.categories] if post.categories else []
        post_dict = post.dict()
        post_dict.pop("categories", None)
        post_dict["category_ids"] = category_ids
        data.append(post_dict)

    return {
        "data": data,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }

@app.get("/posts-pagination/most-commented", tags=["Posts"])
def get_posts_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=10, le=100, description="Quantidade de resultados por página (Por padrão é 10 e seu limite é 100)"),
    session: Session = Depends(get_session)
):
    subq = (
        select(
            Comment.post_id.label("post_id"),
            func.count(Comment.id).label("comment_count")
        )
        .group_by(Comment.post_id)
        .subquery()
    )

    stmt = (
        select(Post, subq.c.comment_count)
        .outerjoin(subq, Post.id == subq.c.post_id)
        .order_by(subq.c.comment_count.desc().nullslast())
    )

    total_records = session.exec(select(func.count(Post.id))).one()
    total_pages = (total_records + page_size - 1)
    offset = (page - 1) * page_size

    if page > total_pages and total_records > 0:
        raise HTTPException(status_code=404, detail="Página não encontrada")
    
    stmt = stmt.offset(offset).limit(page_size)

    rows = session.exec(stmt).all()
    data = []
    for post_obj, comment_count in rows:
        count = comment_count or 0
        post_data = post_obj.dict()
        post_data["comment_count"] = count
        data.append(post_data)

    return {
        "data": data,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }

## Comments
@app.get("/comments-pagination", tags=["Comments"])
def get_comments_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=10, le=100, description="Quantidade de resultados por página (Por padrão é 10 e seu limite é 100)"),
    session: Session = Depends(get_session)
):
    total_records = session.exec(select(func.count(Comment.id))).one()
    total_pages = (total_records + page_size - 1)
    offset = (page -1 ) * page_size

    query = select(Comment).offset(offset).limit(page_size)
    results: List[Comment] = session.exec(query).all()

    return {
        "data": results,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }

## Likes
@app.get("/likes-pagination", tags=["Likes"])
def get_likes_paginated(
    page: int = Query(1, ge=1, description="Número da página (1 por padrão)"),
    page_size: int = Query(10, ge=10, le=100, description="Quantidade de resultados por página (Por padrão é 10 e seu limite é 100)"),
    session: Session = Depends(get_session)
):
    total_records = session.exec(select(func.count(Like.id))).one()
    total_pages = (total_records + page_size - 1)
    offset = (page -1 ) * page_size

    query = select(Like).offset(offset).limit(page_size)
    results: List[Like] = session.exec(query).all()

    return {
        "data": results,
        "pagination": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }