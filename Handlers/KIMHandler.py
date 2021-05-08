from Handlers import ErrorHandler
from Inputs.CLIParser import Params


class KIMHandler:

    def __init__(self, errorHandler: ErrorHandler, cli: dict):
        self._errorHandler = errorHandler
        self._criticalErrorEncountered = False
        self._filesFound: set[str] = set()
        self._cli = cli

    def load(self):
        pass

    def checkFamily(self):
        pass

    def downloadRemote(self):
        pass

    def downloadLocal(self):
        pass

    def launch(self):
        print("####### KIM #######")

        if self._cli[Params.LOAD_KIM]:
            self.load()

        self.checkFamily()

        if not self._criticalErrorEncountered:
            if not self._cli[Params.LOCAL_ONLY]:
                self.downloadRemote()
            if not self._cli[Params.REMOTE_ONLY]:
                self.downloadLocal()

        self._errorHandler.output()
        print("###################\n")

        return self._filesFound
