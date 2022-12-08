from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User
from ..model.List import List
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil


router = APIRouter(prefix="/admin",tags=["ADMIN"])

@router.get("/users/all", response_model=list[User])
async def get_all_users(user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        allUsers = Database.get_users().data
        return allUsers

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all users")
  

@router.delete("/users/delete/{user_id}", status_code=204)
async def delete_user(user_id: int, user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        Database.delete_user_by_id(user_id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting a user")


@router.get("/lists/all", response_model=list[List])
async def get_all_lists(user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        allLists = Database.get_lists()
        return allLists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists")


@router.delete("/lists/delete/{list_id}", status_code=204)
async def delete_list(list_id: int, user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        Database.delete_list_by_id(list_id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting a list")
