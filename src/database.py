import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

db : Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Database:

    def get_users():
        return db.table("users").select("*").execute()

    def create_user(user):
        return db.table("users").insert(user).execute()
    