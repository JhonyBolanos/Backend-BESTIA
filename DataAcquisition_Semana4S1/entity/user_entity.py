from sqlalchemy import Column, Integer, String
from db.config import Base

class UserTable(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key= True)
    correo = Column(String, unique= True)
    password = Column(String)
    role = Column(String)

