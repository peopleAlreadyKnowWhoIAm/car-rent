from typing import List

import flask_sqlalchemy

from repository.basic_repository import BasicRepository
from model.reservation import Reservation


class ReservationRepository(BasicRepository):

    def __init__(self, db_manager: flask_sqlalchemy.SQLAlchemy):
        self.__db_manager = db_manager

    def get_all_entities(self) -> List[Reservation] | None:
        return self.__db_manager.session.query(Reservation).all()

    def get_entity_by_id(self, entity_id: int) -> Reservation | None:
        return self.__db_manager.session.get(entity=Reservation, ident=entity_id)

    def add_entity(self, **kwargs) -> None:
        reservation = Reservation(
            **kwargs
        )
        print(reservation)
        self.__db_manager.session.add(reservation)
        self.__db_manager.session.commit()

    def update_entity(self, entity_id: int, **kwargs):
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        if reservation:
            for key, value in kwargs.items():
                setattr(reservation, key, value)
            print(reservation)
            self.__db_manager.session.commit()

    def delete_entity(self, entity_id: int):
        reservation = self.__db_manager.session.get(entity=Reservation, ident=entity_id)
        print(reservation)
        if reservation:
            self.__db_manager.session.delete(reservation)
            self.__db_manager.session.commit()
