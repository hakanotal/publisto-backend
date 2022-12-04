from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User, UserForgot, UserProfile, UserWithEmail, UserSignUp, UserSignIn, UserWithId, UserToken
from ..model.Token import Token
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil
from ..util.CryptUtil import CryptUtil
from ..util.EmailUtil import EmailUtil
from ..util.ImageUtil import ImageUtil


router = APIRouter(prefix="/user",tags=["USER"])

@router.get("/all", response_model=list[User])
async def get_all_users(user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        allUsers = Database.get_users().data
        return allUsers

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all users")


@router.post("/profile", response_model=UserProfile)
async def get_user_profile(userProfile: UserWithId, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        response = Database.get_user_by_id(userProfile.id)
        userInDb = response.data[0]
        return UserProfile(**userInDb)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while fetching profile")


@router.post("/signup", response_model=Token)
async def sign_up_user(user: UserSignUp):
    try:
        pw = CryptUtil.hash_password(user.password)
        img = ImageUtil.convert_image_to_base64(ImageUtil.generate_image())
        newUser = User(**user.dict(), hashed_password=pw, image=img)
        response = Database.create_user(newUser.dict(exclude_none=True))
        userInDb = UserToken(**response.data[0])
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

        userInDb = UserToken(**response.data[0])
        if CryptUtil.verify_password(user.password, userInDb.hashed_password):
            token = TokenUtil.create_access_token(userInDb) 
            return token
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while signing in user")


@router.post("/reset", status_code=200)
async def send_email_to_reset_password(user: UserWithEmail):
    try:
        response = Database.get_user_by_email(user.email)
        if len(response.data) == 0:
            raise HTTPException(status_code=400, detail="Incorrect email")
        
        EmailUtil.send_reset_password_email(user.email)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while sending email")


@router.post("/verify", response_model=Token)
async def verify_code_to_reset_password(user: UserForgot):
    try:
        if(user.code == "348956"):
            userInDb = Database.get_user_by_email(user.email).data[0]
            updatedUser = User(**userInDb.dict(), hashed_password=CryptUtil.hash_password(user.password))
            
            response = Database.update_user(updatedUser.dict())
            updatedUserInDb = UserToken(**response.data[0])
            return TokenUtil.create_access_token(updatedUserInDb)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while verifying code")


@router.put("/update", response_model=Token)
async def update_user(userUpdate: UserSignUp, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        updatedUser = User(**userUpdate.dict(), id=user.id)
        response = Database.update_user(updatedUser.dict())
        userInDb = UserToken(**response.data[0])
        return TokenUtil.create_access_token(userInDb)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while updating user")
    

@router.delete("/delete", status_code=204)
async def delete_user(userDelete: UserWithId, user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        Database.delete_user_by_id(userDelete.id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting a user")

