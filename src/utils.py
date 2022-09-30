import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, TOKEN_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)