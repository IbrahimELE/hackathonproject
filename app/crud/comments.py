from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.comments import CommentsDB
from schemas.comments import CommentsCreate
from datetime import datetime

def create_comment(db: Session, comment: CommentsCreate):
    db_comment = CommentsDB(
        user_id=comment.user_id,
        post_id=comment.post_id,
        content=comment.content,
        created_at=datetime.now(timezone.utc),
        likes=0  
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_user(db: Session, user_id: int):
    return db.query(CommentsDB).filter(CommentsDB.user_id == user_id).all()

def get_comments_by_post(db: Session, post_id: int):
    return db.query(CommentsDB).filter(CommentsDB.post_id == post_id).all()

def get_comment(db: Session, comment_id: int):
    return db.query(CommentsDB).filter(CommentsDB.id == comment_id).first()

def update_comment(db: Session, comment_id: int, content: str):
    db_comment = db.query(CommentsDB).filter(CommentsDB.id == comment_id).first()
    if db_comment:
        db_comment.content = content
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(CommentsDB).filter(CommentsDB.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return db_comment
    return None

def increment_like_count(db: Session, comment_id: int):
    db_comment = db.query(CommentsDB).filter(CommentsDB.id == comment_id).first()
    if db_comment:
        db_comment.likes += 1
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None
