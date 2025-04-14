from .auth_router import AuthRouter
from .brands_router import BrandsRouter
from .fuel_types_router import FuelTypesRouter
from .register_router import RegisterRouter
from .reports_router import ReportsRouter
from .user_router import UserRouter
from .vehicles_router import VehiclesRouter

__all__ = [
    "AuthRouter",
    "VehiclesRouter",
    "RegisterRouter",
    "ReportsRouter",
    "UserRouter",
    "BrandsRouter",
    "FuelTypesRouter",
]
