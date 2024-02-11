from fastapi import FastAPI, Body, APIRouter, status, HTTPException, Response, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schema
from ..database import get_db

router = APIRouter(prefix="/posts")
@router.get("/", response_model=List[schema.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    # serialize automaticaly the list
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.CreatePost, db: Session = Depends(get_db)):
    # cur.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #             (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM posts WHERE id=%s """, (id,))
    # post = cur.fetchone()
    post = db.query(models.Post).filter_by(id=id).one_or_none()
    if not post:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            detail=f"Post with id {id} is not found")
        # response.status_code = 400
        # return {"message": f"Post with id {id} is not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(""" DELETE FROM posts WHERE id=%s """, (str(id),))
    # row_deleted_count = cur.rowcount
    post = db.query(models.Post).filter_by(id=id).first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    # conn.commit()
    db.delete(post)
    db.commit()
    # with fastapi you dont send content you just send the status
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.UpdatePost, db: Session = Depends(get_db)):
    # cur.execute(""" UPDATE posts
    #             	SET title = %s, content = %s, published = %s
    #              	WHERE id = %s RETURNING * """,
    #             (post.title, post.content, str(post.published), str(id)))
    # updated_post = cur.fetchone()
    updated_post = db.query(models.Post).get(id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    for key, value in post.dict().items():
        setattr(updated_post, str(key), value)
    db.commit()
    db.refresh(updated_post)
    """"
    # same logic for delete
    updated_post = db.query(models.Post).filter_by(id=id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": update_post.first()}
    """
    return updated_post
