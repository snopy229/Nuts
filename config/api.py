from ninja import NinjaAPI

from src.user.router import router as user_router
from src.products.router import router as products_router

api = NinjaAPI()
api.add_router("/user", user_router, tags=["user"])
api.add_router("/products", products_router, tags=["products"])
api.add_router("/checkouts", products_router, tags=["checkouts"])
