from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)  # Ensure price is greater than 0
    cost: float = Field(..., gt=0)  # Ensure cost is greater than 0
    stock: int = Field(..., ge=0)  # Ensure stock is greater than or equal to 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
