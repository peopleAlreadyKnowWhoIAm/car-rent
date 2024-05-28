from repository.basic_repository import BasicRepository
from .report_strategy import ReportStrategy
from constants import SingletonMeta


class ReportContext(metaclass=SingletonMeta):
    __strategy = None

    def set_strategy(self, strategy: ReportStrategy):
        self.__strategy = strategy

    def create_report(self, car_repository: BasicRepository, reservation_repository: BasicRepository):
        if not self.__strategy:
            return None
        return self.__strategy.create_report(car_repository, reservation_repository)
