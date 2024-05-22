from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.car import Car
from constants import OperationStatus


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

    def add_entity(self, **kwargs) -> OperationStatus:
        try:
            car = Car(
                **kwargs
            )
            print(car)
            self.__db_manager.session.add(car)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error adding car:\n{e}")
            return OperationStatus.ERROR

    def update_entity(self, entity_id: int, **kwargs) -> OperationStatus:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        if not car:
            return OperationStatus.NOT_FOUND
        try:
            for key, value in kwargs.items():
                setattr(car, key, value)
            print(car)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when updating car with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def delete_entity(self, entity_id: int) -> OperationStatus:
        car = self.__db_manager.session.get(entity=Car, ident=entity_id)
        if not car:
            return OperationStatus.NOT_FOUND
        try:
            self.__db_manager.session.delete(car)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when deleting car with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def get_filtered_entities(self, **kwargs) -> List[Car] | None:

        try:
            cars = self.__db_manager.session.query(Car).all()
        except Exception as e:
            print(f"Error when getting all cars:\n{e}")
            return None
        if "mode" in kwargs.keys():
            cars = filter(lambda car: car.mode.lower() == kwargs["mode"].lower(), cars)
        if "status" in kwargs.keys():
            cars = filter(lambda car: car.status.lower() == kwargs["status"].lower(), cars)
        if "year_min" in kwargs.keys():
            cars = filter(lambda car: car.year >= int(kwargs["year_min"]), cars)
        if "year_max" in kwargs.keys():
            cars = filter(lambda car: car.year <= int(kwargs["year_max"]), cars)
        if "price_min" in kwargs.keys():
            cars = filter(lambda car: car.price >= int(kwargs["price_min"]), cars)
        if "price_max" in kwargs.keys():
            cars = filter(lambda car: car.price <= int(kwargs["price_max"]), cars)
        return cars
