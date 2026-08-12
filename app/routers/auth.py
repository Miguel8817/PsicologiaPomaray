from fastapi import APIRouter
from models.auth import RegistUserModel
from services.auth import RegistService, loginService

router = APIRouter()

@router.post("/register")
def register_user(data: RegistUserModel):
    return RegistService.register_user(data)

@router.get("/login")
def login_user(data: LoginModel):
    return loginService.login(data)
    
    