from pydantic import BaseModel

class User(BaseModel):
    correo: str
    password: str