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

    # LIST
    def get_lists():
        return db.table("lists").select("*").execute()

    def get_list_by_id(id):
        return db.table("lists").select("*").eq("id", id).execute()
    
    def get_lists_by_user_id(id):
        return db.table("lists").select("*").eq("user_id", id).execute()

    def get_active_lists_by_user_id(id):
        return db.table("lists").select("*").eq("user_id", id).eq("is_active", True).execute()
        
    def create_list(list):
        return db.table("lists").insert(list).execute()

    def update_list(list):
        return db.table("lists").update(list).eq("id", list["id"]).eq("user_id", list["user_id"]).execute()

    def delete_list_by_id(id, user_id):
        return db.table("lists").delete().eq("id", id).eq("user_id", user_id).execute()

    

    
    