from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..database import get_db
from ..models.product import Product
from datetime import datetime
import logging
from typing import List
from ..models.user import User
from ..auth.jwt import get_current_user 
from ..models.farmers import Farmer

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
def create_product(
    product_request: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    farmer = ensure_farmer(db, current_user.id)

    
    product_exists = db.query(Product).filter(Product.name == product_request.name).first()
    if product_exists:
        raiseError(f"Product name '{product_request.name}' already exists")

    
    new_product = Product(
        user_id=current_user.id,
        farmer_id=farmer.id,                      
        name=product_request.name,
        quantity=product_request.quantity,
        price=product_request.price,
        category_id=product_request.category_id
    )

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    except Exception as e:
        raiseError(e)
def ensure_farmer(db: Session, user_id: int) -> Farmer:
    farmer = db.query(Farmer).filter(Farmer.user_id == user_id).first()
    if not farmer:
        farmer = Farmer(user_id=user_id)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
    return farmer

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
# def create_product(product_request: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   


#     product_exists = db.query(Product).filter(Product.name == product_request.name).first()

#     if product_exists:
#         raiseError(f"Product name '{product_request.name}' already exists")
#     new_product = Product(
#         user_id=current_user.id,
#         name=product_request.name,
#         quantity=product_request.quantity,
#         price=product_request.price,
#         category_id=product_request.category_id
#     )
#     try:  
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)

#         return new_product
        
#     except Exception as e:
#         raiseError(e)
# def ensure_farmer(db, user_id: int):
    

#     farmer = db.query(Farmer).filter(Farmer.user_id == user_id).first()
#     if not farmer:
#         farmer = Farmer(user_id=user_id)
#         db.add(farmer)
#         db.commit()
#         db.refresh(farmer)
#     return farmer

@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return products
    except Exception as e:
        raiseError(f"Failed to retrieve products: {e}")

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Product with id {product_id} not found",
                "timestamp": f"{datetime.utcnow()}"
            }
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    
    product_query = db.query(Product).filter(Product.id == product_id)
    existing_product = product_query.first()

    if not existing_product:
        raiseError(f"Product with id {product_id} not found")
    
    
    update_data = product_update.model_dump(exclude_unset=True) 
    try:
        product_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(existing_product)
        
        return existing_product
        
    except Exception as e:
        db.rollback() 
        raiseError(f"Failed to update product: {e}")
    
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    
    product_query = db.query(Product).filter(Product.id == product_id)

    if not product_query.first():
        raiseError(f"Product with id {product_id} not found")
    try:
        product_query.delete(synchronize_session=False)
        db.commit()
       
        return
        
    except Exception as e:
        db.rollback()
        raiseError(f"Failed to delete product: {e}")

@router.get("/user/{user_id}", response_model=List[ProductResponse])
def get_products_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        
        products = db.query(Product).filter(Product.user_id == user_id).all()
        return products 
    except Exception as e:
        raiseError(f"Failed to retrieve products for user {user_id}: {e}")

# def ensure_buyer(db, user_id: int):
#     from ..models.buyer import Buyer

#     buyer = db.query(Buyer).filter(Buyer.user_id == user_id).first()
#     if not buyer:
#         buyer = Buyer(user_id=user_id)
#         db.add(buyer)
#         db.commit()
#         db.refresh(buyer)
#     return buyer
# @router.post("/buy/{product_id}", status_code=status.HTTP_200_OK)
# def buy_product(product_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     product = db.query(Product).filter(Product.id == product_id).first()

#     if not product:
#         raiseError(f"Product with id {product_id} not found")
    
#     if product.quantity < quantity:
#         raiseError(f"Insufficient quantity for product id {product_id}. Available: {product.quantity}, Requested: {quantity}")
    
#     try:
#         product.quantity -= quantity
#         db.commit()
#         db.refresh(product)

#         ensure_buyer(db, current_user.id)

#         return {
#             "status": "success",
#             "message": f"Purchased {quantity} of product id {product_id}",
#             "timestamp": f"{datetime.utcnow()}"
#         }
        
#     except Exception as e:
#         db.rollback()
#         raiseError(f"Failed to purchase product: {e}")