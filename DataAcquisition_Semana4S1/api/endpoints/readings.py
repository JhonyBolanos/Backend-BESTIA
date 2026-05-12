from fastapi import APIRouter
from datetime import datetime

from db.config import SessionLocal
from model.reading_model import Reading
from entity.reading_entity import ReadingTable

router = APIRouter()

# http://localhost:8000/
@router.get("/")
async def root():
    return {"message": "Hello World"}


# http://localhost:8000/example
@router.post("/example")
async def example():
    return {"message": "Hello World"}


# http://localhost:8000/readings
@router.post("/readings")
async def receive_reading(reading: Reading):

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
@router.post("/readings/batch")
async def receive_batch(batch: list[Reading]):

    db = SessionLocal()

    readings_to_save = [
        ReadingTable(
            clave=r.clave,
            acceso=r.acceso,
            timestamp=datetime.fromtimestamp(r.timestamp),
            espacio=r.espacio
        )
        for r in batch
    ]

    db.add_all(readings_to_save)
    db.commit()
    db.close()

    return {
        "message": "Batch saved"
    }