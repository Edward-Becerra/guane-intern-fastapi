from pydantic import BaseModel

class Dog(BaseModel):
    id_dog = int
    name = str
    picture = str
    is_adopted = int
    create_date = str

    class Config:
        orm_mode = True

