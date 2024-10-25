from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db  
from schemas.users import UsersCreate, UsersOut  
from models.users import UsersDB
from models.posts import PostsDB
from models.comments import CommentsDB
from models.likes import LikesDB
from crud.users import create_user, get_user_by_email 
from utils.authentication import create_access_token, verify_password, get_current_user, get_password_hash

load_dotenv()

app = FastAPI()

@app.post("/register", response_model=UsersOut)
def register(user: UsersCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, email_address=user.email_address):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "email": user.email_address,
        "password": get_password_hash(user.password)  
    }
    create_user(db, user_data)  
    return user


@app.get("/users/me", response_model=UsersOut)
async def read_users_me(current_user: UsersOut = Depends(get_current_user)):
    return current_user 
