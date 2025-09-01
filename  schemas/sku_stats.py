from pydantic import BaseModel

class SKUStatsBase(BaseModel):
    sku_id: int
    date: str
    views: int
    orders: int
    sales: float

class SKUStatsCreate(SKUStatsBase):
    pass

class SKUStats(SKUStatsBase):
    id: int

    class Config:
        orm_mode = True