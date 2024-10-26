from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
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
from utils.authentication import  verify_password, get_password_hash
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import Set

load_dotenv()

app = FastAPI()

current_user = None

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Websocket Demo</title>
           <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    </head>
    <body>
    <div class="container mt-3">
        <h1>FastAPI WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="joinChat(event)">
        <input type="text" class="form-control" id="usernameText" placeholder="Enter your username" required autocomplete="off"/>
        <\button class="btn btn-outline-primary mt-2">Join</button>
        </form>
        <ul id='messages' class="mt-5">
        </ul>
        
    </div>
    
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
            function joinChat(event) {
            var username = document.getElementById("usernameText").value;
            client_id = username; // Use username as client_id
            document.querySelector("#ws-id").textContent = client_id;
            ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            event.preventDefault();
            ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            var timestamp = new Date().toLocaleTimeString(); // Get the current time
            var content = document.createTextNode(`[${timestamp}] ${event.data}`);
            message.appendChild(content);
            messages.appendChild(message);
            var typingTimer; // Timer identifier
            var doneTypingInterval = 1000; // Time in ms (1 second)

            // User is typing
            input.addEventListener("keyup", function() {
                clearTimeout(typingTimer);
                ws.send(client_id + " is typing..."); // Send typing message
                typingTimer = setTimeout(doneTyping, doneTypingInterval);
            });

            // User is done typing
            function doneTyping() {
                ws.send(client_id + " stopped typing...");
            }
            };
            }
        </script>
    </body>
</html>
"""
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
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": userdb.username})
    refresh_token = create_refresh_token(data={"sub": userdb.username})

    store_access_token(db, userdb.id, access_token)
    store_refresh_token(db, userdb.id, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/posts")
def create_post(post: PostsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = PostsCreate(title=post.title, content=post.content, user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

blacklisted_tokens: Set[str] = set()  # Store blacklisted tokens in memory for simplicity

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    blacklisted_tokens.add(token)
    return {"message": "Logged out successfully"}

def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens

@app.delete("/delete/my_profile", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user( db: Session = Depends(get_db), current_user: UsersDB = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"detail": "User deleted successfully"}