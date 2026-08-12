from fastapi import HTTPException
from models.auth import LoginModel
from repositories.auth import LoginRepository

class loginService:
    @staticmethod
    def login(data: LoginModel):
        try:
            result = LoginRepository.login(data)
            if not result.data:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontro el usuario"
                )
                
            user = result.data[0]
            if user ["password"] != data.password:
                raise HTTPException(
                    status_code=401,
                    detail="Contraseña incorrecta"
                )
            return user
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al iniciar sesión"
            )
            
class RegistService:
    @staticmethod
    def register_user(data: RegistUserModel):
        try:
            result = RegistUserRepository.register_user(data)
            if result.data:
                raise HTTPException(
                    status_code=400,
                    detail="El usuario ya existe"
                )
            return result
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar el usuario"
            )