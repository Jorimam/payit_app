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

class PaymentCreate(BaseModel):
    order_id: int
    amount: DECIMAL
    payment_type: str
    payment_gateway: str
    payload: Optional[str] = None