import os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from dotenv import load_dotenv
from jose import jwt
from ..model.User import User
from ..model.Token import Token
from ..model.Database import Database

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")


auth_scheme = HTTPBearer()

class TokenUtil:
    
    def create_access_token(data: dict):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, TOKEN_KEY, algorithm=TOKEN_ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")


    async def verify_user_token(token: HTTPBasicCredentials = Depends(auth_scheme)):
        try:
            decodedUser = jwt.decode(token.credentials, TOKEN_KEY, algorithms=TOKEN_ALGORITHM)
            userInDb = Database.get_user_by_id(decodedUser["id"]).data[0]
            return User(**userInDb)
            
        except Exception as e:
            print("[ERROR]", e)
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


    async def verify_admin_token(user: User = Depends(verify_user_token)):
        if not user.is_admin:
            raise HTTPException(status_code=401, detail="Not authorized")
        return user
