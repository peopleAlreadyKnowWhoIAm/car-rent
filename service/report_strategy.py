from abc import ABC, abstractmethod

from constants import ABCSingletonMeta
from repository.basic_repository import BasicRepository


class ReportStrategy(ABC, metaclass=ABCSingletonMeta):
    @abstractmethod
    def create_report(self, car_repository: BasicRepository, reservation_repository: BasicRepository, **kwargs):
        pass
