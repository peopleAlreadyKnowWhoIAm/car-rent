from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.account import Account


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

    def add_entity(self, **kwargs) -> int:
        try:
            account = Account(
                **kwargs
            )
            print(account)
            self.__db_manager.session.add(account)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error adding account:\n{e}")
            return 0

    def update_entity(self, entity_id: int, **kwargs) -> int:
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        if not account:
            return -1
        try:
            for key, value in kwargs.items():
                setattr(account, key, value)
            print(account)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when updating account with id {entity_id}:\n{e}")
            return 0

    def delete_entity(self, entity_id: int) -> int:
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        if not account:
            return -1
        try:
            self.__db_manager.session.delete(account)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when deleting account with id {entity_id}:\n{e}")
            return 0
