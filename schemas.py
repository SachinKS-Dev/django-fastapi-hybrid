# schemas.py

from pydantic import BaseModel


class ItemSchema(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
