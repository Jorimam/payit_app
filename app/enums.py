# ALl enums goes here
from enum import Enum

class Gender(str, Enum):
    male = 'M'
    female = 'F'

class Category(str, Enum):
    buyer = 'buyer'
    farmer = 'farmer'

class ProductCategory(str, Enum):
    tubers = "tubers"
    fruits = "fruits"
    grains = "grains"
    vegetables = "vegetables"
    cereals = "cereals"
    oils = "oils"
    livestock = "livestock"
    latex = "latex"