# Archivo para definir el modelo de la tabla de la base de datos

from sqlalchemy import Column, Integer, String 
from .Conexion import Base

class Dog(Base):
    __tablename__='Dog'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(20))
    picture = Column(String(200))
    is_adopted = Column(Integer)
    create_date = Column(String(200))