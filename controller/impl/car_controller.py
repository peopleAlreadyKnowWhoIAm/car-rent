from typing import Dict

from controller.basic_controller import BasicController
from repository import CarRepository
from constants import OperationStatus


class CarController(BasicController):
    def __init__(self, car_repository: CarRepository):
        self.__repository = car_repository

    def get_all_entities(self) -> Dict:
        cars = self.__repository.get_all_entities()
        if not cars:
            return {"response": "No cars found", "status": 404}
        return {"response": cars, "status": 200}

    def get_entity_by_id(self, entity_id: int) -> Dict:
        car = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not car:
            return {"response": f"No car with id={entity_id} found", "status": 404}
        return {"response": car, "status": 200}

    def get_entity_image_by_id(self, entity_id: int) -> Dict:
        car = self.__repository.get_entity_by_id(entity_id=entity_id)
        if not car:
            return {"response": f"No car with id={entity_id} found", "status": 404}
        return {"response": car.image, "status": 200}

    def add_entity(self, **kwargs) -> Dict:
        operation_status = self.__repository.add_entity(**kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully added car!", "status": 201}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when adding new car. Try again later.", "status": 400}

    def update_entity(self, entity_id: int, **kwargs) -> Dict:
        operation_status = self.__repository.update_entity(entity_id=entity_id, **kwargs)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully updated car!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when updating car. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That car does not exist.", "status": 404}

    def delete_entity(self, entity_id: int) -> Dict:
        operation_status = self.__repository.delete_entity(entity_id=entity_id)
        if operation_status == OperationStatus.SUCCESS:
            return {"response": "Successfully deleted car!", "status": 200}
        if operation_status == OperationStatus.ERROR:
            return {"response": "An error occurred when deleting car. Try again later.", "status": 400}
        if operation_status == OperationStatus.NOT_FOUND:
            return {"response": "That car does not exist.", "status": 404}

    def get_filtered_entities(self, **kwargs) -> Dict:
        cars = self.__repository.get_filtered_entities(**kwargs)
        # if not cars:
        #     return {"response":"No cars found", "status": 404))
        return {"response": cars, "status": 200}
