from Inputs import CLIParser, Params
from Printers import printArgs
from Handlers import ErrorHandler, NISTHandler, KIMHandler

if __name__ == '__main__':
    errorHandler: ErrorHandler = ErrorHandler()
    cli: dict = CLIParser.parse()
    printArgs(cli)

    # Partie NIST
    if not cli[Params.OPENKIM_ONLY]:
        nistHandler: NISTHandler = NISTHandler(errorHandler, cli)
        nistHandler.launch()

    if not cli[Params.NIST_ONLY]:
        kimHandler: KIMHandler = KIMHandler(errorHandler, cli)
        kimHandler.launch()
