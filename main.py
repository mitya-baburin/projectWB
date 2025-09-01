from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


DATABASE_URL = "postgresql+asyncpg://Mitya:Baburin17!@127.0.0.1:5432/database"
Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")

class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="seller")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sku = Column(String)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="products")
    brand = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


app = FastAPI()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.get("/category/{category_name}", response_model=List[Dict[str, Any]])
async def get_category_sales(category_name: str, session: AsyncSession = Depends(get_session)):
    # Fetch category by name
    category = await session.execute(select(Category).filter_by(name=category_name))
    category = category.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")


    products = await session.execute(select(Product).filter_by(category_id=category.id))
    products = products.scalars().all()


    product_list = []
    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "seller": product.seller.name if product.seller else None,
            "brand": product.brand,
            "category_id": product.category_id
        })

    return product_list


@app.get("/sellers/", response_model=List[str])
async def get_all_sellers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Seller.name))
    sellers = result.scalars().all()
    return sellers


@app.get("/sellers/{seller_name}/products/", response_model=List[str])
async def get_seller_products(seller_name: str, session: AsyncSession = Depends(get_session)):
    # Find the seller by name
    seller = await session.execute(select(Seller).filter_by(name=seller_name))
    seller = seller.scalar_one_or_none()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")


    products = await session.execute(select(Product.name).filter_by(seller_id=seller.id))
    products = products.scalars().all()
    return products


@app.get("/products/skus/", response_model=List[str])
async def get_all_skus(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product.sku))
    skus = result.scalars().all()
    return skus