from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas
from ..database import get_db
from ..models import Order, OrderProduct, Product

router = APIRouter()


@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.products:
        raise HTTPException(status_code=400, detail="Order must contain at least one product")

    # Lock all products to prevent inconsistencies in stock
    product_ids = [product.product_id for product in order.products]
    db_products = db.query(Product).filter(Product.id.in_(product_ids)).with_for_update().all()

    # Calculate total price, check stock and decrease it
    total_price = 0
    for db_product in db_products:
        for order_product in order.products:
            if db_product.id == order_product.product_id:
                if db_product.stock < order_product.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for product {db_product.name} (ID: {db_product.id})"
                    )
                db_product.stock -= order_product.quantity
                total_price += db_product.price * order_product.quantity

    order_products = [OrderProduct(product_id=op.product_id, quantity=op.quantity) for op in order.products]

    db_order = Order(
        status=0,  # PENDING
        total_price=total_price,
        created_at=datetime.utcnow(),
        products=order_products
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@router.put("/{order_id}/cancellation", response_model=schemas.Order)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    # Lock order to prevent duplicates cancellations which could lead to increasing stock more than once
    db_order = db.query(Order).filter(Order.id == order_id).with_for_update().first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status != 0:  # PENDING
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")

    # Lock all products and increase stock
    db_products = db.query(Product).join(OrderProduct).filter(OrderProduct.order_id == order_id).with_for_update().all()
    for db_product in db_products:
        for op in db_order.products:
            if db_product.id == op.product_id:
                db_product.stock += op.quantity

    db_order.status = 2  # RETURNED
    db.commit()
    db.refresh(db_order)
    return db_order
