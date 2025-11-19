from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.product import ProductCreateRequest, Product as ProductResponse
from ..database import get_db
from ..models.product import Product
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def raiseError(e):
    logger.error(f"failed to process product request error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to process request: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product_request: ProductCreateRequest, db: Session = Depends(get_db)):
   
    product_exists = db.query(Product).filter(Product.name == product_request.name).first()

    if product_exists:
        raiseError(f"Product name '{product_request.name}' already exists")
    new_product = Product(
        **product_request.model_dump() 
    )
    try:  
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
        
    except Exception as e:
        raiseError(e)

