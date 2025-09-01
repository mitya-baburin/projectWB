from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SKU(Base):
    __tablename__ = "skus"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    category = relationship("Category", back_populates="skus")
    seller = relationship("Seller", back_populates="skus")
    shop = relationship("Shop", back_populates="skus")
    brand = relationship("Brand", back_populates="skus")
    stats = relationship("SKUStats", back_populates="sku")
