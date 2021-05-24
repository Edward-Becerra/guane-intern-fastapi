# Archivo de la implementación

from typing import List
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from . import models
from . import schemas
from .Conexion import SessionLocal, engine
from sqlalchemy.orm import Session

# Para obtener toda la información de los objetos mapeados.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Metodo Get que direcciona a la raiz
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# Metodo Get para listar Dogs
@app.get("api/dogs/",response_model=List[schemas.Dog])
def show_dogs(db:Session=Depends(get_db)):
    dogs = db.query(models.Dog).all()
    return dogs
