from models.auth import LoginModel, RegistUserModel
from utils.db import supabase

class LoginRepository:
    @staticmethod
    def login(data: LoginModel):
        return (
            supabase.table("users").select("*").eq("email", data.email).limit(1).execute()
        )
      
class RegistUserRepository:
    @staticmethod
    def register_user(data: RegistUserModel):
        return (
            supabase.table("users").insert({data.model_dump()}).execute()
        )
            