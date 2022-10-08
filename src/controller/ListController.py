from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User
from ..model.List import List
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil


router = APIRouter(prefix="/list",tags=["LIST"])

@router.get("/all", response_model=list[List])
async def get_all_lists(user: User = Depends(TokenUtil.verify_admin_token)):
    print("[LIST ALL]", user)
    try:
        allLists = Database.get_lists()
        return allLists.data
    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists")


@router.post("/all/user", response_model=list[List])
async def get_all_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    print("[LIST ALL USER]", user)
    try:
        lists = Database.get_lists_by_user_id(user.id)
        return lists.data
    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists of a user")


@router.get("/active/get", response_model=List)
async def get_active_list_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    print("[LIST ACTIVE GET]", user)
    try:
        lists = Database.get_active_list_by_user_id(user.id)
        return lists.data[0]
    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting active list of a user")


