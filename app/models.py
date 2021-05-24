# Archivo para definir el modelo de la tabla de la base de datos

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .Conexion import Base


class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    last_name = Column(String(200))
    email= Column(String(200))
    dogs = relationship("Dog")
    

class Dog(Base):
    __tablename__='dog'
    id_dog = Column(Integer,primary_key=True,index=True)
    name = Column(String(20))
    picture = Column(String(200))
    is_adopted = Column(Boolean)
    create_date = Column(String(200))
    id_user = Column(
        Integer, 
        ForeignKey("user.id_user", ondelete="CASCADE"),
        nullable=False
        )
    
