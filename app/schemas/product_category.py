from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..models.product_category import ProductCategory
from ..enums import ProductCategoryEnum
from ..database import Session as DBsession


class ProductCategorySchema(BaseModel):
    name: ProductCategoryEnum

DEFAULT_CATEGORIES = [cat.value for cat in ProductCategoryEnum]

def init_product_categories():
    db: Session = DBsession()
    for category in DEFAULT_CATEGORIES:
        exists = db.query(ProductCategory).filter_by(name=category).first()
        if not exists:
            db.add(ProductCategory(name=category))
    db.commit()
    db.close()

class Config:
        from_attributes = True
     