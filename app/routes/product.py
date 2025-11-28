from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form
from ..middlewares.auth import AuthMiddleware
from sqlalchemy.orm import Session, defer
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..database import get_db
from ..models.product import Product
from datetime import datetime
import logging
from typing import List
from ..models.user import User
from ..auth.jwt import get_current_user 
from ..models.farmers import Farmer
from ..models.buyers import Buyer
import os 
import aiofiles
from uuid import uuid4

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

UPLOAD_DIR = "/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
def check_farmer(db: Session, user_id: int):
    farmer = db.query(Farmer).filter(Farmer.user_id == user_id).first()
    if not farmer:
        farmer = Farmer(user_id=user_id)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)  
    return farmer

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_product(farmer_id: int= Form(...),
                   category_id: int = Form(...),
                   image: UploadFile = File(...),
                   name: str = Form(...),
                   unit_price : float = Form(...),
                   quantity: int = Form(...),
                   current_user = Depends(AuthMiddleware),
                   db: Session = Depends(get_db)
                   ):
   allowed_extens = ["jpeg", "png", "jpg"]

   file_exten = image.filename.split(".")[-1].lower()

   if not file_exten in allowed_extens:
        raiseError("Invalid file extension. Only jpeg, png, jpg are allowed.")
   try:
        print("====================================")
        file_name = f"{uuid4()}.{file_exten}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        total_size = 0
        img_size = 1024 * 1024

        async with aiofiles.open(file_path, "wb") as outputfile:
            while True:
                content = await image.read(img_size)
                if not content:
                    break
                total_size += len(content)

                if total_size > MAX_FILE_SIZE:
                    raiseError(f"File too large. Max allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB")
                await outputfile.write(content)
   except HTTPException:     
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
   except Exception as e:
        raiseError("This is an internal server error!")

   new_product = Product(
       farmer_id=farmer_id,
       category_id=category_id,
       image_url=file_path,
       name=name,
       quantity=quantity,
       unit_price=unit_price,
    )

   try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "message": "Product uploaded successfully",
            "product": new_product.id,
            "img_url": f"/static/uploads/{file_name}"
        }
   except Exception as e:
        raiseError(e)

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
# def create_product(
#     product_request: ProductCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

  
#     farmer = check_farmer(db, current_user.id)

   
#     product_exists = db.query(Product).filter(Product.name == product_request.name).first()
#     if product_exists:
#         raiseError(f"Product name '{product_request.name}' already exists")

 
#     new_product = Product(
#         farmer_id=farmer.id,
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
def delete_product(product_id: int, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    
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
        farmer = db.query(Farmer).filter(Farmer.user_id == user_id).first()
        if not farmer:
            return []
        products = db.query(Product).filter(Product.farmer_id == farmer.id).all()   
        return products
    except Exception as e:
        raiseError(f"Failed to retrieve products for user {user_id}: {e}")

def ensure_buyer(db, user_id: int):

    buyer = db.query(Buyer).filter(Buyer.user_id == user_id).first()
    if not buyer:
        buyer = Buyer(user_id=user_id)
        db.add(buyer)
        db.commit()
        db.refresh(buyer)
    return buyer
@router.post("/buy/{product_id}", status_code=status.HTTP_200_OK)
def buy_product(product_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raiseError(f"Product with id {product_id} not found")
    
    if product.quantity < quantity:
        raiseError(f"Insufficient quantity for product id {product_id}. Available: {product.quantity}, Requested: {quantity}")
    
    try:
        product.quantity -= quantity
        db.commit()
        db.refresh(product)

        ensure_buyer(db, current_user.id)

        return {
            "status": "success",
            "message": f"Purchased {quantity} of product id {product_id}",
            "timestamp": f"{datetime.utcnow()}"
        }
        
    except Exception as e:
        db.rollback()
        raiseError(f"Failed to purchase product: {e}")