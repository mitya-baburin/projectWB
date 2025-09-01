from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from core.cache import get_cache, set_cache
from models import Category as CategoryDB
from schemas import Category as CategorySchema
import json

router = APIRouter()

@router.get("/{category_id}", response_model=Any)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    cache_key = f"category:{category_id}"
    cached_data = await get_cache(cache_key)

    if cached_data:
        return json.loads(cached_data)

    category = await db.execute(select(CategoryDB).where(CategoryDB.id == category_id))
    category = category.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_schema = CategorySchema.from_orm(category)
    await set_cache(cache_key, json.dumps(category_schema.dict()))

    return [category_schema]