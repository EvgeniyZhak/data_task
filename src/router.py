import aioredis
from schemas import Item
from fastapi import HTTPException, status, APIRouter
import os


router = APIRouter(prefix='/api', tags=['data'])

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

redis = aioredis.from_url(f'redis://{redis_host}:{redis_port}/0')


# Обработчик для получения данных
@router.get("/check_data")
async def check_data(phone: str) -> dict:
    """
    Ручка для получения данных по телефону.
    Возвращает адрес, соответствующий указанному телефону.
    Если такого телефона в бд нет, то возвращает exc 404.
    """
    if address := await redis.get(phone):
        return {"phone": phone, "address": address.decode("utf-8")}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")


# Обработчик для записи данных
@router.post('/write_data')
async def write_data(item: Item) -> dict:
    """
    Ручка для записи данных.
    Принимает телефон и адрес в теле запроса.
    Проверяет, существует ли уже запись с указанным телефоном, если записи нет возвращает exc 404.
    Если запись не прошла возвращает exc 404.
    """
    not_written_exc = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not written",)
    if await redis.exists(item.phone):
        raise not_written_exc

    if await redis.set(item.phone, item.address):
        return {"message": "Data written successfully"}
    raise not_written_exc


# Обработчик для обновления данных
@router.put("/write_data")
async def update_data(item: Item) -> dict:
    """
    Ручка для обновления данных.
    Принимает новый адрес для указанного телефона.
    Проверяет существование записи с указанным телефоном и обновляет адрес, если записи нет возвращает exc 404.
    """
    if await redis.exists(item.phone):
        await redis.set(item.phone, item.address)
        return {"message": "Data updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
