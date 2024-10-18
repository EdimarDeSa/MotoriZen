import uuid
from datetime import date, datetime

from fastapi import APIRouter, Request

from Contents.user_contents import UserMeContent, UserUpdatedContent
from db.Models import NewUserModel, UpdateUserModel, UserModel
from Enums import MotorizenErrorEnum
from ErrorHandler import MotorizenError
from Responses import Created, NoContent, Ok
from Services.user_service import UserService
from Utils.custom_types import CurrentActiveUser

from .base_router import BaseRouter


class UserRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.user_service = UserService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/me", self.me, response_model=UserMeContent, methods=["GET"])
        self.router.add_api_route("/new-user", self.new_user, response_model=UserMeContent, methods=["POST"])
        self.router.add_api_route("/update-user", self.update_user, response_model=UserUpdatedContent, methods=["PUT"])
        self.router.add_api_route("/delete-user", self.delete_user, methods=["DELETE"])

    def me(self, user_data: CurrentActiveUser, request: Request) -> Ok:
        """
        Get the current user

        Examples:

            $curl -X GET \\
            -H "Authorization: Bearer {acess_token}" \\
            http://localhost:8000/users/me
        """
        self.logger.debug("Starting me")

        self.logger.debug(f"User data: {user_data}")

        return Ok(content=UserMeContent(data=user_data), headers=request.headers)

    def new_user(self, request: Request, new_user: NewUserModel) -> Created:
        """
        Create a new user

        Creates a new user.

        Args:

            new_user (NewUserModel): data for the new user.

        Examples:

            $curl -X POST \\
            -H "Content-Type: application/json" \\
            -d '{\\
                    "first_name": "Eduardo", \\
                    "last_name": "Eduardo", \\
                    "email": "email@domain.com",\\
                    "birthdate": "1990-05-15", \\
                    "password": "P@s5W0rd" \\
                }' \\
            http://localhost:8000/users/new-user
        """
        self.logger.debug("Starting new_user")

        try:
            user_data = self.user_service.create_user(new_user)
            content = UserMeContent(data=user_data)

            return Created(content=content, headers=request.headers)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotorizenError):
                e = MotorizenError(err=MotorizenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e.as_http_response()

    def update_user(self, request: Request, user_data: CurrentActiveUser, update_user: UpdateUserModel) -> Ok:
        """
        Update a user

        Updates a user, given the user's access token and the new data.

        Args:

            update_user (UpdateUserModel): new data for the user, all the fields are optional.

        Examples:

            $curl -X PUT \\
            -H "Authorization: Bearer {acess_token}" \\
            -d '{\\ 
                "first_name": "Eduardo",\\ 
                "last_name": "Moreira",\\ 
                "birthdate": "1990-05-15"\\
            }' \\
            http://localhost:8000/users/update-user
        """

        user_updated = self.user_service.update_user(user_data.id_user, update_user)

        content = UserUpdatedContent(data=user_updated)
        return Ok(content=content, headers=request.headers)

    def delete_user(self, request: Request, user_data: CurrentActiveUser) -> NoContent:
        """
        Delete a user

        This function deletes a user, given the user's access token.

        Examples:

            $curl -X DELETE \\
            -H "Authorization: Bearer acess_token" \\
            http://localhost:8000/users/delete-user
        """

        try:

            self.user_service.remove_user(user_data.email, str(user_data.cd_auth))
            return NoContent(headers=request.headers)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotorizenError):
                e = MotorizenError(err=MotorizenErrorEnum.UNKNOWN_ERROR, detail=repr(e), headers=None)

            raise e.as_http_response()
