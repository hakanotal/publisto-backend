from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User, UserSignUp, UserSignIn, UserDelete
from ..model.Token import Token
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil
from ..util.CryptUtil import CryptUtil


router = APIRouter(prefix="/user",tags=["USER"])

@router.get("/all", response_model=list[User])
async def get_all_users(user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        allUsers = Database.get_users().data
        return allUsers

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all users")


@router.post("/signup", response_model=Token)
async def sign_up_user(user: UserSignUp):
    try:
        newUser = User(**user.dict(), hashed_password=CryptUtil.hash_password(user.password))
        response = Database.create_user(newUser.dict(exclude_none=True))
        userInDb = response.data[0]
        return TokenUtil.create_access_token(userInDb)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while signing up user")
    

@router.post("/signin", response_model=Token)
async def sign_in_user(user: UserSignIn):
    try:
        response = Database.get_user_by_email(user.email)

        if len(response.data) == 0:
            raise HTTPException(status_code=400, detail="Incorrect email")

        userInDb = response.data[0]
        if CryptUtil.verify_password(user.password, userInDb["hashed_password"]):
            token = TokenUtil.create_access_token(userInDb) 
            return token
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while signing in user")


@router.put("/update", response_model=User)
async def update_user(userUpdate: UserSignUp,user: User = Depends(TokenUtil.verify_user_token)):
    try:
        updatedUser = User(**userUpdate.dict(), id=user.id)
        response = Database.update_user(updatedUser.dict())
        return response.data[0]

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while updating user")
    

@router.delete("/delete", status_code=204)
async def delete_user(userDelete: UserDelete, user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        Database.delete_user_by_id(userDelete.id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting a user")

