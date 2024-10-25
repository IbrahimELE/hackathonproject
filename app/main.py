from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db  
from schemas.users import UsersCreate, UsersOut, LoginForm
from models.users import UsersDB
from models.posts import PostsDB
from models.comments import CommentsDB
from models.likes import LikesDB
from crud.users import create_user, get_user_by_email 
from utils.authentication import create_access_token, verify_password, get_current_user, get_password_hash

load_dotenv()

app = FastAPI()

@app.get("/test_db_connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")  
        return {"status": "Connected to the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/register", response_model=UsersOut)
def register(user: UsersCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email_address):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "username": user.username,
        "first_name":user.first_name,
        "last_name": user.last_name,
        "email_address": user.email_address,
        "password": get_password_hash(user.password)    
    }
    access_token = create_access_token(data={"sub": user.username})

    create_user(db, user_data)  
    return {"user": user_data, "access_token": access_token, "token-type": "bearer"}

@app.post("/login")
def login( user = LoginForm,  db: Session = Depends(get_db)):
    userdb = get_user_by_email(db, email_address=user.email_address)
    
    if not user or not verify_password(user.password, userdb.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": userdb.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/me", response_model=UsersOut)
async def read_users_me(current_user: UsersOut = Depends(get_current_user)):
    return current_user 


