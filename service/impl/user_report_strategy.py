from collections import Counter
from typing import List

from model.reservation import Reservation
from repository import CarRepository, ReservationRepository
from service.report_strategy import ReportStrategy


class UserReportStrategy(ReportStrategy):
    def __init__(self):
        self.__status_order = {'AVAILABLE': 0, 'RESERVED': 1, 'DAMAGED': 2}

    def create_report(self, car_repository: CarRepository, reservation_repository: ReservationRepository):
        report = {}
        reservations = reservation_repository.get_all_entities()
        reservations = list(filter(lambda reservation: reservation.status != "CANCELED", reservations))
        report["top_cars"] = self.__get_top_cars(reservations, car_repository, limit=5)
        report["cheap_cars"] = self.__get_cheap_cars(car_repository, limit=5)
        report["expensive_cars"] = self.__get_expensive_cars(car_repository, limit=5)
        report["all_cars"] = [car.to_dict() for car in sorted(
            car_repository.get_all_entities(),
            key=lambda car: (self.__status_order.get(car.status, 3), -car.price)
        )]
        return report

    def __get_top_cars(self, reservations: List[Reservation], car_repository: CarRepository, limit: int) \
            -> List[Reservation] | None:
        return [(car_repository.get_entity_by_id(car_id).to_dict(), car_count) for car_id, car_count in
                Counter(reservation.car_id for reservation in
                        filter(lambda reservation: reservation.status != "CANCELED",
                               reservations)
                        ).most_common(limit)] if len(reservations) else None

    def __get_cheap_cars(self, car_repository: CarRepository, limit: int):
        return [car.to_dict() for car in car_repository.get_cheapest_cars(limit)]

    def __get_expensive_cars(self, car_repository: CarRepository, limit: int):
        return [car.to_dict() for car in car_repository.get_most_expensive_cars(limit)]
