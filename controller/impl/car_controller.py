import json

from controller.basic_controller import BasicController
from repository import CarRepository
from flask import Response
from http import HTTPStatus


class CarController(BasicController):
    def __init__(self, car_repository: CarRepository):
        self.__repository = car_repository

    def get_all_entities(self) -> Response:
        cars = self.__repository.get_all_entities()
        if not cars:
            return Response(response="No cars found", status=HTTPStatus(404))
        data = json.dumps([car.to_dict() for car in cars])
        return Response(response=data, status=HTTPStatus(200))

    def get_entity_by_id(self, entity_id: int):
        car = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not car:
            return Response(response=f"No car with id={entity_id} found", status=HTTPStatus(404))
        data = json.dumps(car.to_dict())
        return Response(response=data, status=HTTPStatus(200))

    def add_entity(self, **kwargs):
        self.__repository.add_entity(**kwargs)

    def update_entity(self, entity_id: int, **kwargs):
        self.__repository.update_entity(entity_id=entity_id, **kwargs)

    def delete_entity(self, entity_id: int):
        self.__repository.delete_entity(entity_id=entity_id)
