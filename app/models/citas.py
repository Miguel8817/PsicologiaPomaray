from pydantic import BaseModel
from datetime import date, time

class CitasProfesorModel(BaseModel):
    id_cita_profesor: int
    id_teacher: int
    id_user: int
    name_teacher: str
    FechaCitaProfesor: date
    HoraCitaProfesor: time
    motivo: str
    estado: bool

class CitasPsicologoModel(BaseModel):
    id_cita_psicologo: int
    id_psicologo: int
    id_user: int
    name_psicologo: str
    FechaCitaPsicologo: date
    HoraCitaPsicologo: time
    motivo: str
    estado: bool

class ConfirmCitaPsicologo(BaseModel):
    id_cita_psicologo: int
    id_user: int
    ## Nombre del usuario y su email
    name: str
    email: str
    #El motivo es de la cita con el psicologo 
    motivo: str

class ConfirmCitaProfesor(BaseModel):
    id_cita_profesor: int
    id_user: int
    name: str
    email: str
    motivo: str
