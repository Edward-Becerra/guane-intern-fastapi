# Archivo de la implementación

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse
from . import models
from . import schemas
from .Conexion import SessionLocal, engine
from sqlalchemy.orm import Session
import datetime
import requests
import json


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
@app.get("/api/dogs/",response_model=List[schemas.Dog])
def Show_Dogs(db:Session=Depends(get_db)):
    dogs = db.query(models.Dog).all()
    return dogs


@app.get("/api/dogs/{name}", response_model=schemas.Dog)
def Show_Dogs_By_Name(name:str, db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(name=name).first()
    return dogs


@app.get("/api/dogs/is_adopted/", response_model=List[schemas.Dog])
def Show_Dogs_By_IsAdopted( db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(is_adopted=True).all()
    return dogs


@app.post('/api/dogs/{name}', response_model=schemas.Dog)
def Create_Dog(name: str, entrada: schemas.CreateByName, db: Session = Depends(get_db)):
    
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    if r.status_code  == 200:
        responseApi = json.loads(r.text)
        image = responseApi["message"]
    else :
        image = "api not fount"    

    user = db.query(models.User).filter_by(id_user=entrada.id_user).first()
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No existen registros para id de usuario : ' + str(entrada.id_user))
    else:
        dogs = models.Dog(name=name,
                        picture=image,
                        is_adopted=entrada.is_adopted,
                        create_date=datetime.datetime.now(),
                        id_user = entrada.id_user)
        
        db.add(dogs)
        db.commit()
        db.refresh(dogs)
    return dogs

@app.put('/api/dogs/{name}',response_model=schemas.Dog)
def Update_Dog(name: str, entrada: schemas.UpdateByName, db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(name=name).first()
    user = db.query(models.User).filter_by(id_user=entrada.id_user).first()
    if(dogs == None):
        raise HTTPException(status_code=500, detail='No existen registros para perros de nombre :'+name)
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No es posible actualizar a : '+ name+', ya que no existe usuario de id: ' + str(entrada.id_user))
    else:
        dogs.name = entrada.name
        dogs.is_adopted = entrada.is_adopted
        db.commit()
    db.refresh(dogs)
    return dogs

@app.delete('/api/dogs/{name}',response_model=schemas.Response)
def Delete_Dog(name:str, db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(name=name).first()
    if(dogs == None):
        raise HTTPException(status_code=500, detail='No existen registros para perros de nombre :'+name)
    else:
        db.delete(dogs)
        db.commit()
        response = schemas.Response(message = "Registro elminado con éxito!")
    return response


@app.get('/api/user/', response_model=List[schemas.User])
def Show_Users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/api/user/{id_user}', response_model=schemas.User)
def Show_Users_By_Id(id_user: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter_by(id_user=id_user).first()
    return users



@app.post('/api/user/', response_model=schemas.User)
def Create_Users(entrada: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name = entrada.name, last_name = entrada.last_name, email = entrada.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put('/api/user/{id_user}', response_model=schemas.User)
def Update_Users(id_user: int, entrada: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id_user=id_user).first()
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No existen registros para id de usuario : '+ str(id_user))
    else:
        user.name = entrada.name
        db.commit()
        db.refresh(user)
    return user


@app.delete('/usuarios/{id_user}', response_model=schemas.Response)
def Delete_User(id_user: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id_user=id_user).first()
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No existen registros para id de usuario : '+ str(id_user))
    else:
        db.delete(user)
        db.commit()
        response = schemas.Response(message="Registro elminado con éxito!")
    return response

