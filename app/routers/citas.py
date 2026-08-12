from fastapi import APIRouter
from models.citas import CitasProfesorModel, CitasPsicologoModel
from services.citas import CitasProfesorService, CitasPsicologoService

router = APIRouter()

#Citas profesor
@router.post("/select")
def select_profesor(data: CitasProfesorModel):
    return CitasProfesorService.obtener_citas_profesor(data)

@router.post("/register")
def register_cita(data: CitasProfesorModel):
    return CitasProfesorService.register_cita(data)

@router.put("/update")
def update_cita(data: CitasProfesorModel):
    return CitasProfesorService.update_cita(data)

@router.delete("/delete")
def delete_cita(data: CitasProfesorModel):
    return CitasProfesorService.delete_cita(data)
#-----------------

#Citas psicologo
@router.post("/select")
def select_psicologo(data: CitasPsicologoModel):
    return CitasPsicologoService.obtener_citas_psicologo(data)

@router.post("/register")
def register_cita(data: CitasPsicologoModel):
    return CitasPsicologoService.register_cita(data)

@router.put("/update")
def update_cita(data: CitasPsicologoModel):
    return CitasPsicologoService.update_cita(data)

@router.delete("/delete")
def delete_cita(data: CitasPsicologoModel):
    return CitasPsicologoService.delete_cita(data)
