from fastapi import FastAPI
from .database import engine
from .models.user import User
from .models.product import Product
from .models.base import Base
from .routes.user import router as user_routes
from .routes.product import router as product_routes
from .routes.auth import router as auth
import logging
from .routes import auth
from .schemas.product_category import init_product_categories


logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )

app.include_router(user_routes)
app.include_router(product_routes)
app.include_router(auth.router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hello world"
    }


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    init_product_categories()
