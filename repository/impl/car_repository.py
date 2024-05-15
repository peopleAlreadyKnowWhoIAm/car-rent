from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.car import Car


class CarRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Car] | None:
        try:
            return self.__db_manager.session.query(Car).all()
        except Exception as e:
            print(f"Error when getting all cars:\n{e}")
            return None

    def get_entity_by_id(self, entity_id: int) -> Car | None:
        try:
            return self.__db_manager.session.get(entity=Car, ident=entity_id)
        except Exception as e:
            print(f"Error when getting car with id {entity_id}:\n{e}")
            return None

    def add_entity(self, **kwargs) -> int:
        try:
            car = Car(
                **kwargs
            )
            print(car)
            self.__db_manager.session.add(car)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error adding car:\n{e}")
            return 0

    def update_entity(self, entity_id: int, **kwargs) -> int:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        if not car:
            return -1
        try:
            for key, value in kwargs.items():
                setattr(car, key, value)
            print(car)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when updating car with id {entity_id}:\n{e}")
            return 0

    def delete_entity(self, entity_id: int) -> int:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        if not car:
            return -1
        try:
            self.__db_manager.session.delete(car)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when deleting car with id {entity_id}:\n{e}")
            return 0
