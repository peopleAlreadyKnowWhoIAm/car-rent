import json

from controller.basic_controller import BasicController
from repository import AccountRepository
from flask import Response
from http import HTTPStatus
from constants import OperationStatus


class AccountController(BasicController):
    def __init__(self, account_repository: AccountRepository):
        self.__repository = account_repository

    def get_all_entities(self) -> Response:
        accounts = self.__repository.get_all_entities()
        if not accounts:
            return Response(response="No accounts found", status=HTTPStatus(404))
        data = json.dumps([account.to_dict() for account in accounts])
        return Response(response=data, status=HTTPStatus(200))

    def get_entity_by_id(self, entity_id: int) -> Response:
        account = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not account:
            return Response(response=f"No account with id={entity_id} found", status=HTTPStatus(404))
        data = json.dumps(account.to_dict())
        return Response(response=data, status=HTTPStatus(200))

    def add_entity(self, **kwargs) -> Response:
        operation_status = self.__repository.add_entity(**kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully added account!", status=HTTPStatus(201))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when adding new account. Try again later.", status=HTTPStatus(400))

    def update_entity(self, entity_id: int, **kwargs) -> Response:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully updated account!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when updating account. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That account does not exist.", status=HTTPStatus(404))

    def delete_entity(self, entity_id: int) -> Response:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully deleted account!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when deleting account. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That account does not exist.", status=HTTPStatus(404))
