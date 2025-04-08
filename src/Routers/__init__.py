from .auth_router import AuthRouter
from .brands_router import BrandsRouter
from .cars_router import CarsRouter
from .fuel_types_router import FuelTypesRouter
from .register_router import RegisterRouter
from .reports_router import ReportsRouter
from .user_router import UserRouter

__all__ = [
    "AuthRouter",
    "CarsRouter",
    "RegisterRouter",
    "ReportsRouter",
    "UserRouter",
    "BrandsRouter",
    "FuelTypesRouter",
]
