from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.reservation import Reservation


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

    def add_entity(self, **kwargs) -> int:
        try:
            reservation = Reservation(
                **kwargs
            )
            print(reservation)
            self.__db_manager.session.add(reservation)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error adding reservation:\n{e}")
            return 0

    def update_entity(self, entity_id: int, **kwargs) -> int:
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        if not reservation:
            return -1
        try:
            for key, value in kwargs.items():
                setattr(reservation, key, value)
            print(reservation)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when updating reservation with id {entity_id}:\n{e}")
            return 0

    def delete_entity(self, entity_id: int) -> int:
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        if not reservation:
            return -1
        try:
            self.__db_manager.session.delete(reservation)
            self.__db_manager.session.commit()
            return 1
        except Exception as e:
            print(f"Error when deleting reservation with id {entity_id}:\n{e}")
            return 0
