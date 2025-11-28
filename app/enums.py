# ALl enums goes here
from enum import Enum

class Gender(str, Enum):
    male = 'M'
    female = 'F'

# class Category(str, Enum):
#     buyer = 'buyer'
#     farmer = 'farmer'

class ProductCategoryEnum(str, Enum):
    tubers = "tubers"
    fruits = "fruits"
    grains = "grains"
    vegetables = "vegetables"
    cereals = "cereals"
    oils = "oils"
    livestock = "livestock"
    latex = "latex"
    others = "others"

class OrderStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    delivered = "delivered"
    cancelled = "cancelled"


class PaymentTypeEnum(str, Enum):
    card = "card"
    transfer = "transfer"
    wallet = "wallet"