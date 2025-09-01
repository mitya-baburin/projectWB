from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SKUStats(Base):
    __tablename__ = "sku_stats"
    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(Integer, ForeignKey("skus.id"))
    date = Column(String)
    views = Column(Integer)
    orders = Column(Integer)
    sales = Column(Float)
    sku = relationship("SKU", back_populates="stats")