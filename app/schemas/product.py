from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List, Optional, Dict
from ..enums import Gender
import re
from decimal import Decimal as DECIMAL
from decimal import Decimal
from ..enums import ProductCategoryEnum
from enum import Enum


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    quantity: DECIMAL
    price: DECIMAL
    category_id: int

    model_config = {
        "from_attributes": True
    }
class ProductResponse(BaseModel):
    id: int
    name:str = Field(min_length=3, max_length=20)
    price: Decimal
    quantity: int
    category_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    farmer_id: int

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20) 
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
