from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.account import Account
from constants import OperationStatus


class AccountRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Account] | None:
        try:
            return self.__db_manager.session.query(Account).all()
        except Exception as e:
            print(f"Error when getting all accounts:\n{e}")
            return None

    def get_entity_by_id(self, entity_id: int) -> Account | None:
        try:
            return self.__db_manager.session.get(entity=Account, ident=entity_id)
        except Exception as e:
            print(f"Error when getting account with id {entity_id}:\n{e}")
            return None

    def add_entity(self, **kwargs) -> OperationStatus:
        try:
            account = Account(
                **kwargs
            )
            print(account)
            self.__db_manager.session.add(account)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error adding account:\n{e}")
            return OperationStatus.ERROR

    def update_entity(self, entity_id: int, **kwargs) -> OperationStatus:
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        if not account:
            return OperationStatus.NOT_FOUND
        try:
            for key, value in kwargs.items():
                setattr(account, key, value)
            print(account)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when updating account with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def delete_entity(self, entity_id: int) -> OperationStatus:
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        if not account:
            return OperationStatus.NOT_FOUND
        try:
            self.__db_manager.session.delete(account)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when deleting account with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def get_entity_by_email(self, email: str) -> Account | None:
        return self.__db_manager.session.execute(self.__db_manager.select(Account).filter_by(email=email)).scalar_one_or_none()