from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.car import Car


class CarRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Car] | None:
        return self.__db_manager.session.query(Car).all()

    def get_entity_by_id(self, entity_id: int) -> Car | None:
        return self.__db_manager.session.get(entity=Car, ident=entity_id)

    def add_entity(self, **kwargs) -> None:
        car = Car(
            **kwargs
        )
        print(car)
        self.__db_manager.session.add(car)
        self.__db_manager.session.commit()

    def update_entity(self, entity_id: int, **kwargs) -> None:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        if car:
            for key, value in kwargs.items():
                setattr(car, key, value)
            print(car)
            self.__db_manager.session.commit()

    def delete_entity(self, entity_id: int) -> None:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        print(car)
        if car:
            self.__db_manager.session.delete(car)
            self.__db_manager.session.commit()
