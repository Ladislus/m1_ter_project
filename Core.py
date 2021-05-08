from Inputs import CLIParser, Params
from Printers import printArgs
from Handlers import ErrorHandler, NISTHandler, KIMHandler


def cli():
    settings: dict = CLIParser.parse()
    printArgs(settings)
    main(settings)


def main(settings: dict):
    filesFound: set[str] = set()
    errorHandler: ErrorHandler = ErrorHandler()

    # Partie NIST
    if not settings[Params.OPENKIM_ONLY]:
        nistHandler: NISTHandler = NISTHandler(errorHandler, settings)
        nistFiles: set[str] = nistHandler.launch()
        filesFound = set.union(filesFound, nistFiles)

    if not settings[Params.NIST_ONLY]:
        kimHandler: KIMHandler = KIMHandler(errorHandler, settings)
        kimHandler.launch()

    print("Fichiers trouvés:\n[\n\t{}\n]".format("\n\t".join(filesFound)))


if __name__ == '__main__':
    cli()
