from sqlalchemy.orm import Session
from models.likes import LikesDB
from schemas.likes import LikesCreate

def create_like(db: Session, like: LikesCreate):
    db_like = LikesDB(
        user_id=like.user_id,
        post_id=like.post_id,
        comment_id=like.comment_id,
        type=like.type
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def get_likes_by_user(db: Session, user_id: int):
    return db.query(LikesDB).filter(LikesDB.user_id == user_id).all()

def get_likes_by_post(db: Session, post_id: int):
    return db.query(LikesDB).filter(LikesDB.post_id == post_id).all()

def get_likes_by_comment(db: Session, comment_id: int):
    return db.query(LikesDB).filter(LikesDB.comment_id == comment_id).all()

def delete_like(db: Session, like_id: int):
    db_like = db.query(LikesDB).filter(LikesDB.id == like_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
        return db_like
    return None
