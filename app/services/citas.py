from fastapi import HTTPException
from models.citas import CitasProfesorModel, CitasPsicologoModel
from repositories.citas import CitasProfesorRepository, CitasPsicologoRepository


class CitasProfesorService:

    @staticmethod
    def register_cita(data: CitasProfesorModel):
        try:
            existe = CitasProfesorRepository.obtener_cita(data)

            if existe.data:
                raise HTTPException(
                    status_code=400,
                    detail="La cita ya existe"
                )

            return CitasProfesorRepository.register_cita(data)

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar la cita"
            )


class CitasPsicologoService:

    @staticmethod
    def register_cita(data: CitasPsicologoModel):
        try:
            existe = CitasPsicologoRepository.obtener_cita(data)

            if existe.data:
                raise HTTPException(
                    status_code=400,
                    detail="La cita ya existe"
                )

            return CitasPsicologoRepository.register_cita(data)

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Error al registrar la cita"
            )