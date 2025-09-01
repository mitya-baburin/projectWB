from pydantic import BaseModel

class SKUBase(BaseModel):
    name: str
    category_id: int
    seller_id: int
    shop_id: int
    brand_id: int

class SKUCreate(SKUBase):
    pass

class SKU(SKUBase):
    id: int

    class Config:
        orm_mode = True