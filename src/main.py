from fastapi import FastAPI
from .database import engine, Base
from .products.router import router as products_router
from .orders.router import router as orders_router
from .reports.router import router as reports_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}
