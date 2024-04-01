from pydantic import BaseModel


class Item(BaseModel):
    phone: str
    address: str
