from sqlalchemy import Column, Integer, String, DateTime
from db.config import Base

class ReadingTable(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String)
    acceso = Column(String)
    timestamp = Column(DateTime)
    espacio = Column(String)