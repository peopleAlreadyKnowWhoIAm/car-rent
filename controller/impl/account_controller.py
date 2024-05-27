from typing import Dict

from controller.basic_controller import BasicController
from repository import AccountRepository
from constants import OperationStatus


class AccountController(BasicController):
    def __init__(self, account_repository: AccountRepository):
        self.__repository = account_repository

    def get_all_entities(self) -> Dict:
        accounts = self.__repository.get_all_entities()
        if not accounts:
            return {"response": "No accounts found", "status": 404}
        return {"response": accounts, "status": 200}

    def get_entity_by_id(self, entity_id: int) -> Dict:
        account = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not account:
            return {"response": f"No account with id={entity_id} found", "status": 404}
        return {"response": account, "status": 200}

    def add_entity(self, **kwargs) -> Dict:
        account_result = self.__repository.add_entity(**kwargs)
        if account_result is not None:
            return {"response": account_result, "status": 201}
        else:
            return {"response": "An error occurred when adding new account. Try again later.", "status": 400}

    def update_entity(self, entity_id: int, **kwargs) -> Dict:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully updated account!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when updating account. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That account does not exist.", "status": 404}

    def delete_entity(self, entity_id: int) -> Dict:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully deleted account!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when deleting account. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That account does not exist.", "status": 404}

    def check_entity(self, email: str, password: str) -> Dict:
        reg_acc = self.__repository.get_entity_by_email(email)
        if reg_acc is None:
            return {"response": "Email not registered", "status": 404}
        if reg_acc.password != password:
            return {"response": "Wrong password", "status": 401}
        return {"response": reg_acc, "status": 200}
