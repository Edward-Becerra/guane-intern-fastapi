# Archivo de la implementación

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse
from . import models
from . import schemas
from passlib.hash import bcrypt
from .Conexion import SessionLocal, engine
from sqlalchemy.orm import Session
import datetime
import requests
import json
from app.auth import signJWT
from sqlalchemy.testing.config import db
from app.auth_bearer import JWTBearer


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

#crear usuario
@app.post('/api/user/', dependencies=[Depends(JWTBearer())], response_model=schemas.User)
async def Create_Users(entrada: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name=entrada.name,
                       email=entrada.email,
                       last_name=entrada.last_name, 
                       password=bcrypt.hash(entrada.password)
                       )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    
# login de usuario

@app.post('/api/user/login')
async def user_login(entrada: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter_by(email=entrada.email).first()

    if user == None:
        raise HTTPException(
            status_code=500, detail='No existen el usuario')
   
    if not bcrypt.verify(entrada.password, user.password):
        raise HTTPException(
            status_code=500, detail='Contrasenia incorrecta')
    
    return signJWT(user.email)
    


# listar usuarios
@app.get('/api/user/', response_model=List[schemas.User])
def Show_Users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# mostrar usuario por id
@app.get('/api/user/{id_user}', response_model=schemas.User)
def Show_Users_By_Id(id_user: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter_by(id_user=id_user).first()
    return users

# actualizar usuario
@app.put('/api/user/{id_user}', response_model=schemas.User)
def Update_Users(id_user: int, entrada: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id_user=id_user).first()
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No existen registros para id de usuario : ' + str(id_user))
    else:
        user.name = entrada.name
        db.commit()
        db.refresh(user)
    return user

# eliminar usuario
@app.delete('/usuarios/{id_user}', response_model=schemas.Response)
def Delete_User(id_user: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id_user=id_user).first()
    if(user == None):
        raise HTTPException(
            status_code=500, detail='No existen registros para id de usuario : ' + str(id_user))
    else:
        db.delete(user)
        db.commit()
        response = schemas.Response(message="Registro elminado con éxito!")
    return response

# Crear perro
@app.post('/api/dogs/{name}', dependencies=[Depends(JWTBearer())], response_model=schemas.Dog)
def Create_Dog(name: str, entrada: schemas.CreateByName, db: Session = Depends(get_db)):

    r = requests.get("https://dog.ceo/api/breeds/image/random")
    if r.status_code == 200:
        responseApi = json.loads(r.text)
        image = responseApi["message"]
    else:
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
                          id_user=entrada.id_user)

        db.add(dogs)
        db.commit()
        db.refresh(dogs)
    return dogs

# Metodo Get para listar Dogs
@app.get("/api/dogs/",response_model=List[schemas.Dog])
def Show_Dogs(db:Session=Depends(get_db)):
    dogs = db.query(models.Dog).all()
    return dogs

# Metodo Get para listar Dogs por nombre
@app.get("/api/dogs/{name}", response_model=schemas.Dog)
def Show_Dogs_By_Name(name:str, db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(name=name).first()
    return dogs

# Metodo Get para listar Dogs is adopted
@app.get("/api/dogs/is_adopted/", response_model=List[schemas.Dog])
def Show_Dogs_By_IsAdopted( db: Session = Depends(get_db)):
    dogs = db.query(models.Dog).filter_by(is_adopted=True).all()
    return dogs

# actualizar perro
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

#eliminar perro
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



