import json

from controller.basic_controller import BasicController
from repository import CarRepository
from flask import Response
from http import HTTPStatus
from constants import OperationStatus


class CarController(BasicController):
    def __init__(self, car_repository: CarRepository):
        self.__repository = car_repository

    def get_all_entities(self) -> Response:
        cars = self.__repository.get_all_entities()
        if not cars:
            return Response(response="No cars found", status=HTTPStatus(404))
        data = json.dumps([car.to_dict() for car in cars])
        return Response(response=data, status=HTTPStatus(200))

    def get_entity_by_id(self, entity_id: int) -> Response:
        car = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not car:
            return Response(response=f"No car with id={entity_id} found", status=HTTPStatus(404))
        data = json.dumps(car.to_dict())
        return Response(response=data, status=HTTPStatus(200))
    
    def get_entity_image_by_id(self, entity_id: int) -> Response:
        car = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not car:
            return Response(response=f"No car with id={entity_id} found", status=HTTPStatus(404))
        data = car.image
        return Response(response=data, status=HTTPStatus(200))

    def add_entity(self, **kwargs) -> Response:
        operation_status = self.__repository.add_entity(**kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully added car!", status=HTTPStatus(201))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when adding new car. Try again later.", status=HTTPStatus(400))

    def update_entity(self, entity_id: int, **kwargs) -> Response:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully updated car!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when updating car. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That car does not exist.", status=HTTPStatus(404))

    def delete_entity(self, entity_id: int) -> Response:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully deleted car!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when deleting car. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That car does not exist.", status=HTTPStatus(404))
