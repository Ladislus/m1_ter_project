from Handlers import ErrorHandler
from Inputs import Params
from Databases import NIST


class NISTHandler:

    def __init__(self, errorHandler: ErrorHandler, settings: dict):
        self._errorHandler = errorHandler
        self._criticalErrorEncountered = False
        self._filesFound: set[str] = set()
        self._settings = settings

    def load(self):
        # Partie téléchargement de base de donnée complete
        print("Téléchargement de la base de données NIST complete...")
        NIST.downloadAll(verbose=not self._settings[Params.QUIET])
        print("OK\n")

    def checkFamily(self):
        """
        Méthode qui vérifie que la famille d'intéraction demandée est supportée par le NIST
        """
        # Conversion spéciale de la famille meam/C
        if self._settings[Params.FAMILY] == "meam/c":
            print("Avertissement: Atomman utilise 'meam' à la place de 'meam/c', la famille a donc été changée")
            self._settings[Params.FAMILY] = "meam"

        # Vérification de la validité de la famille demandée
        print("Récupération des familles disponnibles... ", end="")
        families: set[str] = NIST.downloadAllFamilies()
        print("OK")
        if self._settings[Params.VERBOSE]:
            print("Familles disponnibles:\n[ {} ]".format(", ".join(families)))
        if self._settings[Params.FAMILY] not in families:
            self._errorHandler.addError("[CRITIQUE] Familles '{}' non supportée".format(self._settings[Params.FAMILY]))
            self._criticalErrorEncountered = True

    def downloadRemote(self):
        """
        Methode pour la récupération des fichiers potentiels correspondant aux demandes (en distant seulement)
        """
        print("Récupération des potentiels en ligne...")
        filesFound: list[str] = NIST.downloadAllWithFamilyAndElements(
            elements=self._settings[Params.ELEMENTS],
            pair_style=self._settings[Params.FAMILY],
            verbose=not self._settings[Params.QUIET]
        )
        if len(filesFound) > 0:
            print("Articles correspondants trouvés:\n\t{}".format("\n\t".join(filesFound)))
            [self._filesFound.add(fileFound) for fileFound in filesFound]
        else:
            print("Aucun article correspondant n'a été trouvé dans les repertoires distants")
        print("OK\n")

    def downloadLocal(self):
        """
        Methode pour la récupération des fichiers potentiels correspondant aux demandes (en local seulement)
        """
        print("Récupération des potentiels en local...")
        filesFound: list[str] = NIST.queryAllWithFamilyAndElements(
            elements=self._settings[Params.ELEMENTS],
            pair_style=self._settings[Params.FAMILY],
            verbose=not self._settings[Params.QUIET]
        )
        if len(filesFound) > 0:
            print("Articles correspondants trouvés:\n\t{}".format("\n\t".join(filesFound)))
            [self._filesFound.add(fileFound) for fileFound in filesFound]
        else:
            print("Aucun article correspondant n'a été trouvé dans les repertoires locaux")
        print("OK\n")

    def launch(self) -> set[str]:
        print("####### NIST #######")

        if self._settings[Params.LOAD_NIST]:
            self.load()

        self.checkFamily()

        if not self._criticalErrorEncountered:
            if not self._settings[Params.LOCAL_ONLY]:
                self.downloadRemote()
            if not self._settings[Params.REMOTE_ONLY]:
                self.downloadLocal()

        self._errorHandler.output()
        print("####################\n")

        return self._filesFound
