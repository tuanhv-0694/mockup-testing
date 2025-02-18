from pydantic import BaseModel
from datetime import datetime


class ReportParams(BaseModel):
    start_time: datetime
    end_time: datetime


class ReportSummary(BaseModel):
    total_revenue: float
    profit: float
    units_sold: int
    returns: int
