import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


db : Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Database:

    # USER
    def get_users():
        return db.table("users").select("*").execute()

    def create_user(user):
        return db.table("users").insert(user).execute()

    def get_user_by_id(id):
        return db.table("users").select("*").eq("id", id).execute()

    def get_user_by_email(email):
        return db.table("users").select("*").eq("email", email).execute()

    def update_user(user):
        return db.table("users").update(user).eq("id", user["id"]).execute()
        
    def delete_user_by_id(id):
        return db.table("users").delete().eq("id", id).execute()
        
    # LIST
    def get_lists():
        return db.table("lists").select("*").execute()

    def get_list_by_id(id):
        return db.table("lists").select("*").eq("id", id).execute()
    
    def get_lists_by_user_id(id):
        return db.table("lists").select("*").eq("user_id", id).execute()

    def get_joined_lists_by_user_id(id):
        return db.table("users_joined_lists").select("user_id, lists(id,user_id,name,is_active,is_public)").eq("user_id", id).execute()

    def get_active_lists_by_user_id(id):
        return db.table("lists").select("id,user_id,name").eq("user_id", id).eq("is_active", True).execute()

    def get_passive_lists_by_user_id(id):
        return db.table("lists").select("id,user_id,name").eq("user_id", id).eq("is_active", False).execute()

    def get_public_lists_by_user_id(id):
        return db.table("lists").select("id,user_id,name").eq("user_id", id).eq("is_active", True).eq("is_public", True).execute()

    def get_private_lists_by_user_id(id):
        return db.table("lists").select("id,user_id,name").eq("user_id", id).eq("is_active", True).eq("is_public", False).execute()

    def create_list(list):
        return db.table("lists").insert(list).execute()

    def update_list(list):
        return db.table("lists").update(list).eq("id", list["id"]).execute()

    def delete_list_by_id_and_user(id, user_id):
        return db.table("lists").delete().eq("id", id).eq("user_id", user_id).execute()

    def delete_list_by_id(id):
        return db.table("lists").delete().eq("id", id).execute()

    def join_list_by_id(id, user_id):
        return db.table("users_joined_lists").insert({"user_id": user_id, "list_id": id}).execute()

    def leave_list_by_id(id, user_id):
        return db.table("users_joined_lists").delete().eq("user_id", user_id).eq("list_id", id).execute()

    def get_all_items_by_user_id(user_id):
        return db.table("lists").select("items").eq("user_id", user_id).execute()

    
    