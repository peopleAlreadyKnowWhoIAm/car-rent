import json

from controller.basic_controller import BasicController
from repository import ReservationRepository
from flask import Response
from http import HTTPStatus
from constants import OperationStatus


class ReservationController(BasicController):
    def __init__(self, reservation_repository: ReservationRepository):
        self.__repository = reservation_repository

    def get_all_entities(self) -> Response:
        reservations = self.__repository.get_all_entities()
        if not reservations:
            return Response(response="No reservations found", status=HTTPStatus(404))
        data = json.dumps([reservation.to_dict() for reservation in reservations])
        return Response(response=data, status=HTTPStatus(200))

    def get_entity_by_id(self, entity_id: int) -> Response:
        reservation = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not reservation:
            return Response(response=f"No reservation with id={entity_id} found", status=HTTPStatus(404))
        data = json.dumps(reservation.to_dict())
        return Response(response=data, status=HTTPStatus(200))

    def add_entity(self, **kwargs) -> Response:
        operation_status = self.__repository.add_entity(**kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully added reservation!", status=HTTPStatus(201))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when adding new reservation. Try again later.", status=HTTPStatus(400))

    def update_entity(self, entity_id: int, **kwargs) -> Response:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully updated reservation!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when updating reservation. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That reservation does not exist.", status=HTTPStatus(404))

    def delete_entity(self, entity_id: int) -> Response:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return Response(response="Successfully deleted reservation!", status=HTTPStatus(200))
        if operation_status == OperationStatus.ERROR:
            return Response(response="An error occurred when deleting reservation. Try again later.", status=HTTPStatus(400))
        if operation_status == OperationStatus.NOT_FOUND:
            return Response(response="That reservation does not exist.", status=HTTPStatus(404))
