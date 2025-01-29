from pydantic import BaseModel
from typing import List

class User(BaseModel):
    member_id: int
    member_name: str
    books_quantity: int
    books_owned: List[str]
    total_price: float

class User_1(BaseModel):
    books_owned: str

class BorrowBooks(BaseModel):
    books_owned: List[str]###model