from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
from typing import List, Optional, Dict
from ..enums import Gender, Category
import re
from decimal import Decimal as DECIMAL

class Product(BaseModel):
    id:int
    user_id: int
    name: str 
    quantity_kg: DECIMAL
    price_per_kg: DECIMAL

class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    quantity_kg: DECIMAL
    price_per_kg: DECIMAL



    