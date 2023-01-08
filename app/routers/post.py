from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# from typing import Optional, List - check python version
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models, schemas, ouauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db),
                 current_user: int = Depends(ouauth2.get_current_user)):
    # cur.execute('''INSERT INTO public.posts (title, content, published)
    #            VALUES (%s, %s, %s)''',
    #            (post.title, post.content, post.published))

    # new_post = cur.fetchone()
    # conn.commit()
    # ---------------------
    # ineficienet_way = models.Posts(title=post.title, content=post.content, published=post.published)
    new_post = models.Posts(user_id=current_user.id, **post.dict())
    db.add(new_post)  # Adds to database
    db.commit()  # Commit changes
    db.refresh(new_post)  # Retrieve and store in new_post (RETURNIG *)

    return new_post


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: str | None = "",
              current_user: int = Depends(ouauth2.get_current_user)):
    # cur.execute('''SELECT * FROM public.posts''')
    # posts = cur.fetchall()
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(
        models.Posts, func.count(models.Likes.posts_id).label("Likes")
    ).join(
        models.Likes,
        models.Likes.posts_id == models.Posts.id,
        isouter=True
    ).group_by(
        models.Posts.id
    ).filter(
        models.Posts.title.contains(search)
    ).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: int = Depends(ouauth2.get_current_user)):

    # cur.execute('''SELECT * FROM public.posts WHERE id = %s''', (str(id),))
    # post = cur.fetchone()

    post = db.query(
        models.Posts, func.count(models.Likes.posts_id).label("Likes")
    ).join(
        models.Likes,
        models.Likes.posts_id == models.Posts.id,
        isouter=True
    ).group_by(
        models.Posts.id
    ).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(ouauth2.get_current_user)):

    # cur.execute('''DELETE FROM public.posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()

    post = db.query(models.Posts).filter(models.Posts.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} does not exist"
        )

    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot deleat this post!"
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: int = Depends(ouauth2.get_current_user)):

    # cur.execute('''UPDATE public.posts SET title = %s, content = %s, published = %s
    #            WHERE id = %s RETURNING *''',
    #            (post.title, post.content, post.published, str(id),))
    #
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} does not exist"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot deleat this post!"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
