class ErrorHandler:

    def __init__(self):
        self._errors: list[str] = []
        self._errorCount = 0

    def addError(self, error: str) -> None:
        self._errors.append(error)
        self._errorCount += 1

    def hasError(self) -> bool:
        return self._errorCount > 0

    def getErrorCount(self) -> int:
        return self._errorCount

    def clear(self) -> None:
        self._errors = []
        self._errorCount = 0

    def output(self) -> None:
        if self.hasError():
            print("⚠️ Errors ⚠️")
            for i in range(self._errorCount):
                print("\tError {}: {}".format(i, self._errors[i]))
            self.clear()
        else:
            print("No errors")
