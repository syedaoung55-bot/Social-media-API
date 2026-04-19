from .. import models, schems, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schems.PostOut])
def get_posts(db: Session = Depends(get_db),  current_user: int =
    Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, 
    search: Optional[str]= ""):
    # cursor.execute(""" SELECT * FROM post """), we can also we ?limit=something in our postman
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == 
        models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #return [{"Post": post, "votes": votes} for post, votes in posts]
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schems.Post)
def create_posts(post: schems.PostCreate, db: Session = Depends(get_db), current_user: int =
                Depends(oauth2.get_current_user) ):
    # cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) 
    #                returning *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #title= post.title, content= post.content, published= post.published
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())  # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #for reurning of sql in orm
    return new_post 


@router.get("/{id}", response_model=schems.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db),  current_user: int =
                Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == 
        models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  current_user: int =
                Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post Where id = %s""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to perform that action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schems.Post)
def update_post(id: int, updated_post: schems.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to perform that action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False) # pyright: ignore[reportArgumentType]
    db.commit()
    return post_query.first()