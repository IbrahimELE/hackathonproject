from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.posts import PostsDB
from schemas.posts import PostsCreate
from datetime import datetime

def create_post(db: Session, post: PostsCreate):
    db_post = PostsDB(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
        created_at=datetime.now(timezone.utc),
        post_status=post.post_status
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, user_id: str):
    return db.query(PostsDB).filter(PostsDB.user_id == user_id).all()

def get_post(db: Session, post_id: int):
    return db.query(PostsDB).filter(PostsDB.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostsCreate):
    db_post = db.query(PostsDB).filter(PostsDB.id == post_id).first()
    if db_post:
        for key, value in post.model_dump().items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
        return db_post
    return None

def delete_post(db: Session, post_id: int):
    db_post = db.query(PostsDB).filter(PostsDB.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post
    return None
