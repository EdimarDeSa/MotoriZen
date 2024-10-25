from Services.base_service import BaseService


class RegisterService(BaseService):
    def __init__(self) -> None:
        self.create_logger(__name__)
        self._register_repository = RegisterRepository()
        self._cache_handler = RedisHandler()
