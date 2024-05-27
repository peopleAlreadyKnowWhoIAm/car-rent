from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.reservation import Reservation, ReservationStatus
from constants import OperationStatus


class ReservationRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Reservation] | None:
        try:
            return self.__db_manager.session.query(Reservation).all()
        except Exception as e:
            print(f"Error when getting all reservations:\n{e}")
            return None

    def get_entity_by_id(self, entity_id: int) -> Reservation | None:
        try:
            return self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        except Exception as e:
            print(f"Error when getting reservation with id {entity_id}:\n{e}")
            return None

    def add_entity(self, **kwargs) -> OperationStatus:
        try:
            reservation = Reservation(
                **kwargs
            )
            print(reservation)
            self.__db_manager.session.add(reservation)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error adding reservation:\n{e}")
            return OperationStatus.ERROR

    def update_entity(self, entity_id: int, **kwargs) -> OperationStatus:
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        if not reservation:
            return OperationStatus.NOT_FOUND
        try:
            for key, value in kwargs.items():
                setattr(reservation, key, value)
            print(reservation)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when updating reservation with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def delete_entity(self, entity_id: int) -> OperationStatus:
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        if not reservation:
            return OperationStatus.NOT_FOUND
        try:
            self.__db_manager.session.delete(reservation)
            self.__db_manager.session.commit()
            return OperationStatus.SUCCESS
        except Exception as e:
            print(f"Error when deleting reservation with id {entity_id}:\n{e}")
            return OperationStatus.ERROR

    def get_entities_by_account_id(self, account_id: int) -> List[Reservation] | None:
        try:
            return self.__db_manager.session.query(Reservation).filter(Reservation.user_id == account_id).all()
        except Exception as e:
            print(f"Error when getting all reservations for user with ID {account_id}:\n{e}")
            return None

    def get_ongoing_reservation_by_car_id(self, car_id: int) -> List[Reservation] | None:
        try:
            return self.__db_manager.session.query(Reservation).filter(Reservation.car_id == car_id,
                                                                       Reservation.status not in [
                                                                           ReservationStatus.CANCELED,
                                                                           ReservationStatus.COMPLETED
                                                                       ]).all()
        except Exception as e:
            print(f"Error when getting all reservations for car with ID {car_id}:\n{e}")
            return None
