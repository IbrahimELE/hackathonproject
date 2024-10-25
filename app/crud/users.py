from sqlalchemy.orm import Session
from models.users import UsersDB
from schemas.users import UsersCreate
import bcrypt

def create_user(db: Session, user: UsersCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = UsersDB(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        password=hashed_password.decode("utf-8"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email_address: str):
    return db.query(UsersDB).filter(UsersDB.email_address == email_address).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
