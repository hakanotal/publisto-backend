import datetime as dt
from fastapi import APIRouter, HTTPException, Depends
from ..model.User import User
from ..model.List import List, ListCreate, ListUpdate, ListWithId
from ..model.Database import Database
from ..util.TokenUtil import TokenUtil


router = APIRouter(prefix="/list",tags=["LIST"])


@router.get("/user", response_model=list[List])
async def get_all_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting all lists of the user")


@router.get("/joined", response_model=list[List])
async def get_all_joined_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        joined_lists = Database.get_joined_lists_by_user_id(user.id).data
        id_list = [list['list_id'] for list in joined_lists]
        lists = Database.get_lists_by_id_list(id_list)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting joined lists of the user")


@router.get("/active", response_model=list[List])
async def get_all_active_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_active_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting active lists of the user")


@router.get("/passive", response_model=list[List])
async def get_all_passive_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_passive_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting passive lists of the user")


@router.get("/public", response_model=list[List])
async def get_all_public_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_public_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting public lists of the user")


@router.get("/private", response_model=list[List])
async def get_all_private_lists_of_a_user(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        lists = Database.get_private_lists_by_user_id(user.id)
        return lists.data

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while getting private lists of the user")


@router.get("/recommend", response_model=str)
async def get_a_recipe_recommendation(user: User = Depends(TokenUtil.verify_user_token)):
    try:
        return "TODO: This is a recipe recommendation"
            
    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while fetching a recipe recommendation")


@router.post("/create", response_model=List)
async def create_list_for_a_user(list: ListCreate, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        newList = List(**list.dict(), user_id=user.id, updated_at=str(dt.datetime.now()))
        response = Database.create_list(newList.dict(exclude_none=True))
        listInDb = response.data[0]
        return listInDb

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while creating list for the user")


@router.put("/update", response_model=List)
async def update_list_of_a_user(list: ListUpdate, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        updatedList = List(**list.dict(), user_id=user.id, updated_at=str(dt.datetime.now()))
        response = Database.update_list(updatedList.dict())
        listInDb = response.data[0]
        return listInDb

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while updating list of the user")


@router.delete("/delete", status_code=204)
async def delete_list_of_a_user(list: ListWithId, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        Database.delete_list_by_id_and_user(list.id, user.id)

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while deleting list of the user")


@router.post("/join", response_model=List)
async def join_to_a_list(list: ListWithId, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        listInDb = Database.get_list_by_id(list.id).data[0]
        if listInDb['is_public'] and listInDb['user_id'] != user.id:
            Database.join_list_by_id(list.id, user.id)
            return listInDb
        else:
            raise Exception()

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while joining to the list")


@router.delete("/leave", status_code=204)
async def leave_a_list(list: ListWithId, user: User = Depends(TokenUtil.verify_user_token)):
    try:
        Database.leave_list_by_id(list.id, user.id)
            
    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=400, detail="Error while leaving the list")
