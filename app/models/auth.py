from pydantic import BaseModel

class LoginModel(BaseModel):
    email: str
    password: str

class RegistUserModel(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    phone: str
    
