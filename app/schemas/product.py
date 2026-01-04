from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal as DECIMAL


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    quantity: DECIMAL
    unit_price: DECIMAL
    category_id: int

    model_config = {
        "from_attributes": True
    }
class ProductResponse(ProductCreate):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    farmer_id: int

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20) 
    unit_price: Optional[DECIMAL] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
