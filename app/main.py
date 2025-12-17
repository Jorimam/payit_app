from fastapi import FastAPI
from .database import engine
from .models.user import User
from .models.product import Product
from .models.base import Base
from .routes.user import router as user_routes
from .routes.product import router as product_routes
from .routes.auth import oauth as oauth_routes
import logging
from .schemas.product_category import init_product_categories
from .routes.auth import router as auth_routes
from .routes.oauth import router as oauth_routes
import os 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )

def db_and_table_init():
    retries = 30
    for i in range(retries):
        try:
            logger.info("Initializing database...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialization successful.")
            break
        except Exception as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries})...")
            logger.error(f"Error: {e}")
            time.sleep(3)

@app.on_event("startup")
def on_startup():
    db_and_table_init()


app.include_router(user_routes)
app.include_router(product_routes)
app.include_router(oauth_routes)
app.include_router(auth_routes)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv, #("SESSION_SECRET_KEY", "123"),
    https_only=False,
)
origins = ["http://localhost:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hello world or Logout successfully"
    }


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    init_product_categories()
