from abc import ABC, abstractmethod

from controller.basic_controller import BasicController


class ReportStrategy(ABC):
    @abstractmethod
    def create_report(self, controller: BasicController, **kwargs):
        pass


class UserReportStrategy(ReportStrategy):
    def create_report(self, controller: BasicController, **kwargs):
        pass


class ManagerReportStrategy(ReportStrategy):
    def create_report(self, controller: BasicController, **kwargs):
        pass
