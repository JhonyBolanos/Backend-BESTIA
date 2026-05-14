from fastapi import APIRouter
from datetime import datetime

from db.config import SessionLocal
from model.reading_model import Reading
from model.reading_model import OpenRoomRequest
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

@router.get("/readings")
async def get_readings():
    db = SessionLocal()

    readings = db.query(ReadingTable).order_by(ReadingTable.id.desc()).all()

    result = []
    for r in readings:
        result.append({
            "id": r.id,
            "clave": r.clave,
            "acceso": r.acceso,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None,
            "espacio": r.espacio
        })

    db.close()

    return result


#AQUI SE HACE LA LOGICA PARA QUE SE MUESTREN LOS DATOS EN EL FRONT Y SE PUEDA ABRIR UNA SALA SIENDO ADMINd



@router.post("/admin/open-room")
async def open_room(request: OpenRoomRequest):
    db = SessionLocal()

    reading_to_save = ReadingTable(
        clave="",
        acceso="valido",
        timestamp=datetime.now(),
        espacio=request.espacio
    )

    db.add(reading_to_save)
    db.commit()
    db.refresh(reading_to_save)
    db.close()

    return {
        "message": "Sala abierta manualmente",
        "id": reading_to_save.id,
        "clave": reading_to_save.clave,
        "acceso": reading_to_save.acceso,
        "timestamp": reading_to_save.timestamp.isoformat(),
        "espacio": reading_to_save.espacio
    }