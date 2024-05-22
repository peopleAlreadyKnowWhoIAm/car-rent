class ReportContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def create_report(self, **kwargs):
        self._strategy.create_report(**kwargs)
