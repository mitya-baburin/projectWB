import asyncio
import aiohttp
import openpyxl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import logging
from sqlalchemy import select
from models import Category, Seller, Product

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sku = Column(String)
    seller = Column(String)
    brand = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', category_id={self.category_id})>"


DATABASE_URL = "postgresql+asyncpg://Mitya:Baburin17!@127.0.0.1:5432/database"
engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_data(api_url: str):
    try:
        logging.info(f"Запрос к API: {api_url}")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                logging.info(f"Статус код ответа: {response.status}")
                logging.info(f"Content type: {response.headers.get('Content-Type')}")
                content = await response.read()
                logging.debug(f"Размер контента: {len(content)} байт")
                try:
                    with open("temp.xlsx", "wb") as f:
                        f.write(content)
                    workbook = openpyxl.load_workbook("temp.xlsx")
                    logging.debug("Excel файл успешно загружен")
                    sheet = workbook.active
                    headers = [cell.value for cell in sheet[1]]
                    logging.debug(f"Заголовки: {headers}")
                    data = []
                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        data.append(dict(zip(headers, row)))
                    logging.debug(f"Загруженные данные: {data}")
                    return data
                except Exception as e:
                    logging.error(f"Ошибка при обработке Excel файла: {e}")
                    return None
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return None
    except openpyxl.utils.exceptions.InvalidFileException as e:
        logging.error(f"Ошибка при обработке Excel файла: {e}")
        return None
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        return None


async def add_products_to_db(data: list[dict]):
    async with AsyncSession(engine) as session:
        for item in data:
            try:

                category_name = item.get('Основная категория', 'Default Category')
                if not category_name:
                    logging.warning(f"Пропущена категория для продукта: {item.get('Название', 'Без названия')}")
                    continue


                result = await session.execute(select(Category).filter_by(name=category_name))
                category = result.scalar_one_or_none()

                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                    await session.commit()
                    logging.info(f"Добавлена новая категория: {category_name}")

                product = Product(
                    name=item.get('Название', 'Default Product Name'),
                    sku=item.get('SKU', '0000'),
                    seller=item.get('Продавец', 'Unknown Seller'),
                    brand=item.get('Бренд', 'Unknown Brand'),
                    category_id=category.id,
                    category=category
                )
                session.add(product)
            except Exception as e:
                logging.error(f"Ошибка при добавлении продукта {item.get('Название', 'Без названия')}: {e}")
                await session.rollback()
        await session.commit()
        print("Products added successfully!")

async def main():
    await create_db_and_tables()

    API_URL = "https://analitika.woysa.club/images/panel/json/download/niches.php?skip=0&price_min=0&price_max=1060225&up_vy_min=0&up_vy_max=108682515&up_vy_pr_min=0&up_vy_pr_max=2900&sum_min=1000&sum_max=82432725&feedbacks_min=0&feedbacks_max=32767&trend=false&sort=sum_sale&sort_dir=-1&id_cat=10000"
    data = await load_data(API_URL)
    if data:
        await add_products_to_db(data)
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    asyncio.run(main())


