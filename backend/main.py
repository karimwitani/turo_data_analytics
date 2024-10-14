from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session
from models.sqlalchemy_models import Base, Item
from models.search_page_models import TuroSearchRequestModel
from schemas import ItemCreate, ItemRead


# Dependency
async def get_db():
    async with async_session() as session:
        yield session

app = FastAPI()

@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item




if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
