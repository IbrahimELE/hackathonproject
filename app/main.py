from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db  
from schemas.users import UsersCreate, UsersOut, LoginForm, User
from schemas.posts import Posts, PostsCreate
from models.users import UsersDB
from models.posts import PostsDB
from schemas.likes import Likes
from models.comments import CommentsDB
from models.likes import LikesDB
from crud.users import create_user, get_user_by_email, get_user_by_username
from utils.authentication import create_access_token, verify_password, get_current_user, get_password_hash, create_refresh_token, store_refresh_token, store_access_token
from utils.authentication import oauth2_scheme
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import Set

load_dotenv()

app = FastAPI()

current_user = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["192.168.122.247:5173", "http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/test_db_connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  
        return {"status": "Connected to the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/register")
def register(user: UsersCreate):
    db = next(get_db())
    if get_user_by_email(db, user.email_address) or get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    hash_password = get_password_hash(user.password)
    random_id = random.randint(0, 255)

    user_data = UsersDB(
        id=random_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        password=hash_password,
    )
    
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return {"user": user_data, "message": "success"}

@app.post("/login")
def login(user: LoginForm):
    db = next(get_db())
    userdb = get_user_by_email(db, user.email_address)

    global current_user

    if not userdb or not verify_password(user.password, userdb.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    current_user = {
        "username": userdb.username,
        "email_address": userdb.email_address,
        "id": userdb.id,
    }
    return {"message": "Login successful"}

@app.post("/posts")
def create_post(post: PostsCreate):
    global current_user 
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not logged in")

    db = next(get_db())  
    db_post = PostsDB(title=post.title, content=post.content, user_id=current_user["id"], created_at=post.created_at, post_status=post.post_status)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.post("/logout")
def logout():
    global current_user
    current_user = None
    return {"message": "Logged out successfully"}

@app.delete("/delete/my_profile", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user():
    db = next(get_db())
    db.delete(current_user)
    db.commit()
    return {"detail": "User deleted successfully"}