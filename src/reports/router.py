from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import schemas
from ..database import get_db

router = APIRouter()


@router.get("/summary", response_model=schemas.ReportSummary)
def get_report_summary(params: schemas.ReportParams = Depends(), db: Session = Depends(get_db)):
    start = params.start_time
    end = params.end_time

    result = db.execute(text("""
        SELECT
            SUM(CASE WHEN o.status != 2 THEN op.quantity * p.price ELSE 0 END) AS total_revenue,
            SUM(CASE WHEN o.status != 2 THEN op.quantity * (p.price - p.cost) ELSE 0 END) AS profit,
            SUM(CASE WHEN o.status != 2 THEN op.quantity ELSE 0 END) AS units_sold,
            SUM(CASE WHEN o.status = 2 THEN op.quantity ELSE 0 END) AS returns
        FROM (
            SELECT id, status, created_at
            FROM orders
            WHERE created_at >= :start AND created_at <= :end
        ) o
        JOIN order_products op ON o.id = op.order_id
        JOIN products p ON op.product_id = p.id
    """), {"start": start, "end": end}).fetchone()

    return {
        "total_revenue": result.total_revenue or 0,
        "profit": result.profit or 0,
        "units_sold": result.units_sold or 0,
        "returns": result.returns or 0
    }
