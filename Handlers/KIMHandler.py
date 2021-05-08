from Handlers import ErrorHandler
from Inputs import Params


class KIMHandler:

    def __init__(self, errorHandler: ErrorHandler, settings: dict):
        self._errorHandler = errorHandler
        self._criticalErrorEncountered = False
        self._filesFound: set[str] = set()
        self._settings = settings

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

        if self._settings[Params.LOAD_KIM]:
            self.load()

        self.checkFamily()

        if not self._criticalErrorEncountered:
            if not self._settings[Params.LOCAL_ONLY]:
                self.downloadRemote()
            if not self._settings[Params.REMOTE_ONLY]:
                self.downloadLocal()

        self._errorHandler.output()
        print("###################\n")

        return self._filesFound
