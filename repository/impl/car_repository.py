from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.car import Car, CarMode, CarStatus
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
        if "mode" in kwargs:
            cars = filter(lambda car: car.mode == CarMode[kwargs["mode"].upper()], cars)
        if "status" in kwargs:
            cars = filter(lambda car: car.status == CarStatus[kwargs["status"].upper()], cars)
        if "year_from" in kwargs:
            cars = filter(lambda car: car.year >= int(kwargs["year_from"]), cars)
        if "year_to" in kwargs:
            cars = filter(lambda car: car.year <= int(kwargs["year_to"]), cars)
        if "price_from" in kwargs:
            cars = filter(lambda car: car.price >= int(kwargs["price_from"]), cars)
        if "price_to" in kwargs:
            cars = filter(lambda car: car.price <= int(kwargs["price_to"]), cars)
        if "search" in kwargs:
            search_query = kwargs["search"].lower()
            cars = filter(lambda car: search_query in car.model.lower() or search_query in car.brand.lower(), cars)
        return cars

    def get_most_expensive_cars(self, limit=3):
        cars = self.__db_manager.session.query(Car).order_by(Car.price.desc()).limit(limit).all()
        return cars

    def get_cheapest_cars(self, limit=3):
        cars = self.__db_manager.session.query(Car).order_by(Car.price.asc()).limit(limit).all()
        return cars
