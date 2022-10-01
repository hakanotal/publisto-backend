from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from typing import Optional
from .database import Database
from pydantic import BaseModel
from .token import TokenUtil, Token
from .crypt import CryptUtil


class User(BaseModel):
    is_admin: Optional[bool] = False
    name: str
    email: str
    hashed_password: str

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

class UserSignIn(BaseModel):
    email: str
    password: str

auth_scheme = HTTPBearer()


router = APIRouter()

async def decode_token(token: HTTPBasicCredentials = Depends(auth_scheme)):
    try:
        decodedUser = TokenUtil.decode_access_token(token.credentials)
        userInDb = Database.get_user_by_id(decodedUser["id"]).data[0]
        return User(**userInDb)
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


@router.get("/user/all", response_model=list[User])
async def get_users(user: User = Depends(decode_token)):
    if user.is_admin:
        print("[USER ALL]", user)
        allUsers = Database.get_users()
        return allUsers.data


@router.post("/user/signup", response_model=Token)
async def sign_up_user(user: UserSignUp):
    print("[USER SIGN_UP] ", user)

    try:
        newUser = User(**user.dict(), hashed_password=CryptUtil.hash_password(user.password))
        response = Database.create_user(newUser)
        userInDb = response.data[0]
        return TokenUtil.create_access_token(userInDb)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while signing up user")
    

@router.post("/user/signin", response_model=Token)
async def sign_in_user(user: UserSignIn):
    print("[USER SIGN_IN] ", user)

    try:
        response = Database.get_user_by_email(user.email)

        if len(response.data) == 0:
            raise HTTPException(status_code=400, detail="Incorrect email")

        userInDb = response.data[0]
        if CryptUtil.verify_password(user.password, userInDb["hashed_password"]):
            token = TokenUtil.create_access_token(userInDb) 
            print(token)
            return token
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while signing in user")
    