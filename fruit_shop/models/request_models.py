from pydantic import BaseModel
from typing_extensions import Dict


class AddSale(BaseModel):
    shop_name: str
    date: str
    items: Dict[str, int]


class JWTHeader(BaseModel):
    user_jwt: str
