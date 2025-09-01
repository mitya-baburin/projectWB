from pydantic import BaseModel

class ShopBase(BaseModel):
    name: str

class ShopCreate(ShopBase):
    pass

class Shop(ShopBase):
    id: int

    class Config:
        orm_mode = True