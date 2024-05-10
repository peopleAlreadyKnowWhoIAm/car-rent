from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.account import Account


class AccountRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Account] | None:
        return self.__db_manager.session.query(Account).all()

    def get_entity_by_id(self, entity_id: int) -> Account | None:
        return self.__db_manager.session.get(entity=Account, ident=entity_id)

    def add_entity(self, **kwargs) -> None:
        account = Account(
            **kwargs
        )
        print(account)
        self.__db_manager.session.add(account)
        self.__db_manager.session.commit()

    def update_entity(self, entity_id: int, **kwargs):
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        if account:
            for key, value in kwargs.items():
                setattr(account, key, value)
            print(account)
            self.__db_manager.session.commit()

    def delete_entity(self, entity_id: int):
        account = self.__db_manager.session.get(entity=Account, ident=entity_id)
        print(account)
        if account:
            self.__db_manager.session.delete(account)
            self.__db_manager.session.commit()
