from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.config import Base, engine
from api.endpoints.readings import router as readings_router

app = FastAPI()


#CONEXION DE CORS (API)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(readings_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
