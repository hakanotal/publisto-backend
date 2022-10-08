import datetime as dt
from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User
from ..model.List import List, ListCreate, ListUpdate, ListDelete
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil


router = APIRouter(prefix="/list",tags=["LIST"])

@router.get("/all", response_model=list[List])
async def get_all_lists(user: User = Depends(TokenUtil.verify_admin_token)):
    try:
        allLists = Database.get_lists()
        return allLists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists")


@router.get("/all/user", response_model=list[List])
async def get_all_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists of a user")


@router.get("/all/active", response_model=list[List])
async def get_all_active_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_active_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting active list of a user")


@router.post("/create", response_model=List)
async def create_list_for_a_user(list: ListCreate, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        newList = List(**list.dict(), user_id=user.id, updated_at=str(dt.datetime.now()))
        response = Database.create_list(newList.dict(exclude_none=True))
        listInDb = response.data[0]
        return listInDb

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while creating list for a user")


@router.put("/update", response_model=List)
async def update_list_of_a_user(list: ListUpdate, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        updatedList = List(**list.dict(), user_id=user.id, updated_at=str(dt.datetime.now()))
        response = Database.update_list(updatedList.dict())
        listInDb = response.data[0]
        return listInDb

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while updating list of a user")


@router.delete("/delete", status_code=204)
async def delete_list_of_a_user(list: ListDelete, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        Database.delete_list_by_id(list.id, user.id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting list of a user")

