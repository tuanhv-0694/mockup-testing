from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas
from ..database import get_db
from ..models import Product

router = APIRouter()


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if product.price <= 0 or product.cost <= 0 or product.stock < 0:
        raise HTTPException(status_code=400, detail="Invalid product data")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
@router.patch("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    if product.price <= 0 or product.cost <= 0 or product.stock < 0:
        raise HTTPException(status_code=400, detail="Invalid product data")
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
