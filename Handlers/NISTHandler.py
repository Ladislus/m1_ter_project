from Errorhandler import ErrorHandler
from Inputs.CLIParser import Params
from Databases import NIST


class NISTHandler:

    def __init__(self, errorHandler: ErrorHandler, cli: dict):
        self._errorHandler = errorHandler
        self._criticalErrorEncountered = False
        self._filesFound: set[str] = set()
        self._cli = cli

    def load(self):
        # Partie téléchargement de base de donnée complete
        NIST.downloadAll(verbose=not self._cli[Params.QUIET])

    def checkFamily(self):
        """
        Méthode qui vérifie que la famille d'intéraction demandée est supportée par le NIST
        """
        # Conversion spéciale de la famille meam/C
        if self._cli[Params.FAMILY] == "meam/c":
            print("Avertissement: Atomman utilise 'meam' à la place de 'meam/c', la famille a donc été changée")
            self._cli[Params.FAMILY] = "meam"

        # Vérification de la validité de la famille demandée
        print("Récupération des familles disponnibles... ", end="")
        families: set[str] = NIST.getAllPairStyles()
        print("OK")
        if self._cli[Params.VERBOSE]:
            print("Familles disponnibles:\n[ {} ]".format(", ".join(families)))
        if self._cli[Params.FAMILY] not in families:
            self._errorHandler.addError("[CRITIQUE] Familles '{}' non supportée".format(self._cli[Params.FAMILY]))
            self._criticalErrorEncountered = True

    def downloadRemote(self):
        """
        Methode pour la récupération des fichiers potentiels correspondant aux demandes (en distant seulement)
        """
        print("Récupération des potentiels en ligne...")
        fileFound: str = NIST.downloadOneWithFamilyAndElements(
            elements=self._cli[Params.ELEMENTS],
            pair_style=self._cli[Params.FAMILY]
        )
        if fileFound is not None:
            self._filesFound.add(fileFound)
            if self._cli[Params.VERBOSE]:
                print("Chemin local vers le dossier de l'article: {}".format(fileFound))
        print("OK")

    def downloadLocal(self):
        """
        Methode pour la récupération des fichiers potentiels correspondant aux demandes (en local seulement)
        """
        print("Récupération des potentiels en local...")
        potentialsId: list[str] = NIST.query_elements(elements=self._cli[Params.ELEMENTS])
        paths: list[str] = []
        for potentialId in potentialsId:
            paths.extend(NIST.get_absolute_path_potential(potentialId))
        if self._cli[Params.VERBOSE]:
            print("Chemins locaux:", end="")
            for path in paths:
                print("\n\t{}".format(path))
        print("OK\n")

    def launch(self) -> set[str]:
        print("####### NIST #######")

        if self._cli[Params.LOAD_NIST]:
            self.load()

        if not self._criticalErrorEncountered:
            if not self._cli[Params.LOCAL_ONLY]:
                self.downloadRemote()
            if not self._cli[Params.REMOTE_ONLY]:
                self.downloadLocal()

        self._errorHandler.output()
        print("####################\n")

        return self._filesFound
