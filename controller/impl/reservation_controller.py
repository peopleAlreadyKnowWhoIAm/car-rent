from typing import Dict

from controller.basic_controller import BasicController
from repository import ReservationRepository
from constants import OperationStatus
from model.reservation import ReservationStatus


class ReservationController(BasicController):
    def __init__(self, reservation_repository: ReservationRepository):
        self.__repository = reservation_repository

    def get_all_entities(self) -> Dict:
        reservations = self.__repository.get_all_entities()
        if not reservations:
            return {"response": "No reservations found", "status": 404}
        return {"response": reservations, "status": 200}

    def get_entity_by_id(self, entity_id: int) -> Dict:
        reservation = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not reservation:
            return {"response": f"No reservation with id={entity_id} found", "status": 404}
        return {"response": reservation, "status": 200}

    def add_entity(self, **kwargs) -> Dict:
        operation_status = self.__repository.add_entity(**kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully added reservation!", "status": 201}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when adding new reservation. Try again later.", "status": 400}

    def update_entity(self, entity_id: int, **kwargs) -> Dict:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully updated reservation!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when updating reservation. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That reservation does not exist.", "status": 404}

    def delete_entity(self, entity_id: int) -> Dict:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully deleted reservation!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when deleting reservation. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That reservation does not exist.", "status": 404}

    def get_all_entities_by_account_id(self, account_id: int) -> Dict:
        reservations = self.__repository.get_entities_by_account_id(account_id=account_id)
        return {"response": reservations, "status": 200}

    def get_ongoing_reservation_by_car_id(self, car_id: int) -> Dict:
        reservations = self.__repository.get_ongoing_reservation_by_car_id(car_id)
        return {"response": reservations, "status": 200}
