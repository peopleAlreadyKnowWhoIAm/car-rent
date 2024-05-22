from controller.basic_controller import BasicController
from manager.report_strategy import ReportStrategy


class ReportContext:
    def __init__(self, strategy: ReportStrategy):
        self.__strategy = strategy

    def set_strategy(self, strategy: ReportStrategy):
        self.__strategy = strategy

    def create_report(self, controller: BasicController, **kwargs):
        self.__strategy.create_report(controller=controller, **kwargs)
