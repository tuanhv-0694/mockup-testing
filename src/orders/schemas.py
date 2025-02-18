from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class OrderProductBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)  # Ensure quantity is greater than 0


class OrderProductCreate(OrderProductBase):
    pass


class OrderProduct(OrderProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: int  # 0: PENDING, 1: COMPLETED, 2: RETURNED
    total_price: float
    created_at: datetime


class OrderCreate(BaseModel):
    products: List[OrderProductCreate]


class Order(OrderBase):
    id: int
    products: List[OrderProduct]

    class Config:
        orm_mode = True
