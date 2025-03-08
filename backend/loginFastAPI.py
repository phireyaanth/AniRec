from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
import sqlite3
import jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body


# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Secret Key
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    anime_list TEXT DEFAULT ''
)
""")
conn.commit()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class AnimeListUpdate(BaseModel):
    anime_list: List[str]

# Helper functions
def get_user(username: str):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def create_user(username: str, password: str):
    hashed_password = pwd_context.hash(password)  # Hash the password before storing
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str):
    expiration = datetime.utcnow() + timedelta(days=1)
    return jwt.encode({"sub": username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API Routes
@app.post("/register")
def register(user: UserCreate = Body()):
    if create_user(user.username, user.password):
        return {"message": "User created successfully"}
    raise HTTPException(status_code=400, detail="Username already taken")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user[2]):  # Verify password correctly
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(user[1])  # Generate JWT token
    return {"access_token": token, "token_type": "bearer"}



@app.get("/profile")
def get_profile(user: tuple = Depends(get_current_user)):
    return {"username": user[1], "anime_list": user[3].split(',') if user[3] else []}

@app.post("/profile")
def update_profile(anime_list: AnimeListUpdate, user: tuple = Depends(get_current_user)):
    cursor.execute("UPDATE users SET anime_list = ? WHERE username = ?", (','.join(anime_list.anime_list), user[1]))
    conn.commit()
    return {"message": "Anime list updated"}