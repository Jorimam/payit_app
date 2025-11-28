from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..middlewares.auth import AuthMiddleware
from ..models import user_model, products, orders, buyers
from ..schemas.orders import Order
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Orders"])

@router.post("/orders")
def order_product(order: Order, current_user=Depends(AuthMiddleware), db: Session= Depends(get_db)):
    available_product = db.query(products.Product).filter(products.Product.name == order.product_name).first()
    if not available_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product is out of stock"
        )

    new_buyer = db.query(buyers.Buyer).filter(buyers.Buyer.user_id == current_user.id)
    new_buyer = buyers.Buyer(user_id = current_user.id)
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    
    new_order = orders.Order(
        **order.model_dump(exclude={"product_name"}),
        product_id = available_product.id,
        buyer_id = new_buyer.id,
        unit_price = available_product.unit_price,
        order_status = "pending",
        amount = available_product.unit_price * order.quantity
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/orders/{order_id}")
def get_an_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(orders.Order).filter(orders.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order with ID not found"
        )

    return order


@router.delete("/orders/{order_id}")
def cancel_order(order_id: int, current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    check_buyer = db.query(buyers.Buyer).filter(buyers.Buyer.user_id == current_user.id).first()
    if not check_buyer:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Buyer with ID not found"
        )
    check_order = db.query(orders.Order).filter(orders.Order.id == order_id).first()
    if not check_order:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order with ID not found!"
        )

    if check_order.order_status.value == 'delivered':
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Order is already processed!"
            )
    else:
        db.delete(check_order)
        db.commit()
        raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Order cancelled!"
        )

    
@router.get("/orders")
def get_all_orders(db: Session=Depends(get_db)):
    return db.query(orders.Order).all()
   