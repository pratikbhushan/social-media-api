from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from typing import List
from .. import schemas, model, oauth2
from sqlalchemy.orm import Session 
from ..database import get_db


router = APIRouter(
    prefix= '/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post_Response])
def get_posts(db: Session = Depends(get_db), limit: int = 10):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(limit)
    posts = db.query(model.Post).limit(limit).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post_Response)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = model.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post_Response)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()

    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(model.Post).filter(model.Post.id == id)

    post = deleted_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action.")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@router.put("/{id}")
def update_post(id:int, post: schemas.Post_Create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    update_post = post_query.first()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if update_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action.")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": update_post}