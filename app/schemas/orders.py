from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List, Optional, Dict
from decimal import Decimal as DECIMAL
from enum import Enum

class OrdersCreate(BaseModel):
    buyer_id: int
    product_id: int
    quantity: DECIMAL
    unit_price: DECIMAL
    total_price: DECIMAL
    order_status: Optional[str] = "pending"