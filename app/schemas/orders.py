from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List, Optional, Dict
from ..enums import Category
import re
from decimal import Decimal as DECIMAL
from decimal import Decimal
from ..enums import ProductCategory
from enum import Enum

class OrdersCreate(BaseModel):
    buyer_id: int
    product_id: int
    quantity: DECIMAL
    unit_price: DECIMAL
    total_price: DECIMAL
    order_status: Optional[str] = "pending"