import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


db : Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Database:

    def get_users():
        return db.table("users").select("*").execute()

    def create_user(user):
        return db.table("users").insert(user).execute()

    def get_user_by_id(id):
        return db.table("users").select("*").eq("id", id).execute()

    def get_user_by_email(email):
        return db.table("users").select("*").eq("email", email).execute()

    def get_lists():
        return db.table("lists").select("*").execute()
    
    def get_lists_by_user_id(user_id):
        return db.table("lists").select("*").eq("user_id", user_id).execute()

    def get_active_list_by_user_id(user_id):
        return db.table("lists").select("*").eq("user_id", user_id).eq("is_active", True).execute()
    
    