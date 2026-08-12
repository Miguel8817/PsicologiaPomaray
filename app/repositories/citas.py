from pydantic import BaseModel
from models.citas import CitasProfesorModel, CitasPsicologoModel, ConfirmCitaPsicologo, ConfirmCitaProfesor
from utils.db import conexion

##Citas profesor

class CitasProfesorRepository:

    @staticmethod
    def insertar_cita(data: CitasProfesorModel):
        return (
            supabase
            .table("citas_profesor")
            .insert(data.model_dump())
            .execute()
        )

    @staticmethod
    def obtener_citas(data: CitasProfesorModel):
        return (
            supabase
            .table("citas_profesor")
            .select("*")
            .eq("id_user", data.id_user)
            .execute()
        )

    @staticmethod
    def eliminar_cita(data: CitasProfesorModel):
        return (
            supabase
            .table("citas_profesor")
            .delete()
            .eq("id_cita_profesor", data.id_cita_profesor)
            .execute()
        )

    @staticmethod
    def actualizar_cita(data: CitasProfesorModel):
        return (
            supabase
            .table("citas_profesor")
            .update(
                data.model_dump(
                    exclude={"id_cita_profesor"}
                )
            )
            .eq("id_cita_profesor", data.id_cita_profesor)
            .execute()
        )
#----------------------------------

##Citas psicologo
class CitasPsicologoRepository:

    @staticmethod
    def insertar_cita(data: CitasPsicologoModel):
        return (
            supabase
            .table("citas_psicologo")
            .insert(data.model_dump())
            .execute()
        )

    @staticmethod
    def obtener_citas(data: CitasPsicologoModel):
        return (
            supabase
            .table("citas_psicologo")
            .select("*")
            .eq("id_user", data.id_user)
            .execute()
        )

    @staticmethod
    def eliminar_cita(data: CitasPsicologoModel):
        return (
            supabase
            .table("citas_psicologo")
            .delete()
            .eq("id_cita_psicologo", data.id_cita_psicologo)
            .execute()
        )

    @staticmethod
    def actualizar_cita(data: CitasPsicologoModel):
        return (
            supabase
            .table("citas_psicologo")
            .update(
                data.model_dump(exclude={"id_cita_psicologo"})
            )
            .eq("id_cita_psicologo", data.id_cita_psicologo)
            .execute()
        )
        
class ConfirmCitaPsicologoRepository:

    @staticmethod
    def obtener_cita(data: ConfirmCitaPsicologo):
        return (
            supabase
            .table("confirm_cita_psicologo")
            .select("*")
            .eq("id_cita_psicologo", data.id_cita_psicologo)
            .execute()
        )

    @staticmethod
    def actualizar_cita(data: ConfirmCitaPsicologo):
        return (
            supabase
            .table("confirm_cita_psicologo")
            .update(
                data.model_dump(
                    exclude={"id_cita_psicologo"}
                )
            )
            .eq("id_cita_psicologo", data.id_cita_psicologo)
            .execute()
        )

class ConfirmCitaProfesorRepository:

    @staticmethod
    def obtener_cita(data: ConfirmCitaProfesor):
        return (
            supabase
            .table("confirm_cita_profesor")
            .select("*")
            .eq("id_cita_profesor", data.id_cita_profesor)
            .execute()
        )

    @staticmethod
    def actualizar_cita(data: ConfirmCitaProfesor):
        return (
            supabase
            .table("confirm_cita_profesor")
            .update(
                data.model_dump(
                    exclude={"id_cita_profesor"}
                )
            )
            .eq("id_cita_profesor", data.id_cita_profesor)
            .execute()
        )