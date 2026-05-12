from pydantic import BaseModel

class Reading(BaseModel):
    clave: str
    acceso: str
    timestamp: int
    espacio: str