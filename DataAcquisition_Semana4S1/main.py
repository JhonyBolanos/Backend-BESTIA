import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime
from datetime import datetime


# Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_CfK7A2GmDTZc@ep-plain-star-aib8yvpj-pooler.c-4.us-east-1.aws.neon.tech/neondb")
#DATABASE_URL = "postgresql://neondb_owner:npg_CfK7A2GmDTZc@ep-plain-star-aib8yvpj-pooler.c-4.us-east-1.aws.neon.tech/neondb"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# Modelo de Datos 
class ReadingTable(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String)
    acceso = Column(String)
    timestamp = Column(DateTime)
    espacio = Column(String)

# APP
app = FastAPI()

#Modelo de datos
class Reading(BaseModel):
    clave: str
    acceso: str
    timestamp: int
    espacio: str


# https://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://localhost:8000/example
@app.post("/example")
async def example():
    return {"message": "Hello World"}


# http://localhost:8000/readings
# {"value":514, "timestamp":200, "deviceName":"Temp01", "units":"celsius"}
@app.post("/readings")
async def receive_reading(reading:Reading):
    db = SessionLocal()
    fecha = datetime.fromtimestamp(reading.timestamp)
    reading_to_save = ReadingTable(
        clave=reading.clave,
        acceso=reading.acceso,
        timestamp=fecha,
        espacio=reading.espacio
    )
    db.add(reading_to_save)
    db.commit()
    db.refresh(reading_to_save)
    db.close()
    return {
        "message": "Reading received",
        "clave": reading.clave,
        "acceso": reading.acceso 
    }

# http://localhost:8000/readings/batch
# [{}, {}, {}]
# [{"value":514, "timestamp":200, "deviceName":"Temp01", "units":"celsius"}, {"value":514, "timestamp":200, "deviceName":"Temp01", "units":"celsius"}, {"value":514, "timestamp":200, "deviceName":"Temp01", "units":"celsius"}]
@app.post("/readings/batch")
async def receive_batch(batch:list[Reading]):
    db = SessionLocal()

    readigns_to_save = [ReadingTable(
        value = r.value,
        timestamp = r.timestamp,
        deviceName = r.deviceName,
        units = r.units
    ) for r in batch]
    # List[reading] -> List[readingTable]
    # Para poder almacenarlo en SQL

    db.add_all(readigns_to_save)
    db.commit()
    db.close()
    return{
        "message" : "Batch saved",
    }

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)