from Handlers import ErrorHandler


class KIMHandler:

    def __init__(self, errorHandler: ErrorHandler, cli: dict):
        self._errorHandler = errorHandler
        self._cli = cli
        print("####### KIM #######")

    def launch(self):
        pass
