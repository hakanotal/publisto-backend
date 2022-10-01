import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt
from pydantic import BaseModel

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenUtil:
    
    def create_access_token(data: dict):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, TOKEN_KEY, algorithm=TOKEN_ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")

    def decode_access_token(token: str):
        return jwt.decode(token, TOKEN_KEY, algorithms=TOKEN_ALGORITHM)
