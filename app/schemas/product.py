from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List, Optional, Dict
from ..enums import Gender, Category
import re
from decimal import Decimal as DECIMAL
from decimal import Decimal
from ..enums import ProductCategory
from enum import Enum


class ProductCategory(str, Enum):
    grains = "grains"
    tubers = "tubers"
    vegetables = "vegetables"
    fruits = "fruits"
    livestock = "livestock"
    cereals = "cereals"
    oils = "oils"
    latex = "latex"
    
class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    quantity: DECIMAL
    price: DECIMAL
    ProductCategory: ProductCategory

class ProductResponse(BaseModel):
    id: int
    name:str = Field(min_length=3, max_length=20)
    price: Decimal
    quantity: int
    ProductCategory: ProductCategory
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20) 
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    category: Optional[ProductCategory] = None

class Config:
        
        from_attributes = True 
     

    