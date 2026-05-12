from fastapi import FastAPI

from db.config import Base, engine
from api.endpoints.readings import router as readings_router

app = FastAPI()

app.include_router(readings_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
