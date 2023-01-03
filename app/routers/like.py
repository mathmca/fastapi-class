from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, ouauth2
from ..database import get_db

router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Likes, current_user: int = Depends(ouauth2.get_current_user),
              db: Session = Depends(get_db)):
    like_query = db.query(models.Likes).filter(
            models.Likes.user_id == current_user.id, 
            models.Likes.posts_id == like.post_id
        )
    found_like = like_query.first()
    
    if (like.dir == 1):
        if (found_like):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already liked on {like.post_id}"
            )
            
        new_like = models.Likes(user_id=current_user.id, posts_id=like.post_id)
        db.add(new_like)
        db.commit()
        
        return {"message": "successfully liked"}
    else:
        if (not found_like):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )
        
        like_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "liked successfully deleted"}