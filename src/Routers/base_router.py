import logging
from abc import ABC, abstractmethod

from fastapi import APIRouter

from Utils.Internacionalization import InternationalizationManager


class BaseRouter(ABC):
    def __init__(self) -> None:
        self.__router: APIRouter | None = None
        self.__logger: logging.Logger | None = None
        self.__txt_manager: InternationalizationManager | None = None

    @property
    def router(self) -> APIRouter:
        if self.__router is None:
            raise Warning("Initialize the router first using self.router = APIRouter(...)")
        return self.__router

    @router.setter
    def router(self, value: APIRouter) -> None:
        if not isinstance(value, APIRouter):
            raise TypeError("Router must be an instance of APIRouter")
        self.__router = value

    @abstractmethod
    def _register_routes(self) -> None:
        pass

    @property
    def logger(self) -> logging.Logger:
        if self.__logger is None:
            raise Warning("Initialize the logger first using self.logger = self.create_logger(__name__)")
        return self.__logger

    @logger.setter
    def logger(self, value: logging.Logger) -> None:
        if not isinstance(value, logging.Logger):
            raise TypeError("Logger must be an instance of logging.Logger")
        self.__logger = value

    @property
    def txt_manager(self) -> InternationalizationManager:
        if self.__txt_manager is None:
            raise Warning(
                "Initialize the internationalization manager first using self.txt_manager = InternationalizationManager()"
            )
        return self.__txt_manager

    @txt_manager.setter
    def txt_manager(self, value: InternationalizationManager) -> None:
        if not isinstance(value, InternationalizationManager):
            raise TypeError("Internationalization manager must be an instance of InternationalizationManager")
        self.__txt_manager = value

    def create_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)
