from CLIParser import parse, Params
from ArgumentPrinter import print_parameters
import NIST
from Errorhandler import ErrorHandler
from GUI import fenetrePrincipale

if __name__ == '__main__':
    errors: ErrorHandler = ErrorHandler()
    cli: dict = parse()
    print_parameters(cli)

    # Partie téléchargement de base de donnée complete
    if cli[Params.LOAD_NIST]:
        if cli[Params.QUIET]:
            NIST.download_all_lammps_potentials(verbose=False)
        else:
            NIST.download_all_lammps_potentials(verbose=True)

    if cli[Params.LOAD_KIM]:
        # TODO lors du merge avec Kim
        pass

    # Partie NIST
    if not cli[Params.OPENKIM_ONLY]:
        print("####### NIST #######")

        # Conversion spéciale de la famille meam/C
        if cli[Params.FAMILY] == "meam/c":
            print("Warning: Atomman uses 'meam' as the 'meam/c' family")
            cli[Params.FAMILY] = "meam"

        # Vérification de la validité de la famille demandée
        print("Récupération des familles disponnibles... ", end="")
        families: set[str] = NIST.getAllPairStyles()
        print("OK")
        if cli[Params.VERBOSE]:
            print("Familles disponnibles:\n[ {} ]".format(", ".join(families)))
        if cli[Params.FAMILY] not in families:
            errors.addError("[CRITICAL] Familles '{}' non supportée".format(cli[Params.FAMILY]))
            errors.output()
            exit(1)

        # Recherche en ligne
        if not cli[Params.LOCAL_ONLY]:
            print("Récupération des potentiels en ligne...")
            articleId: str = NIST.download_lammps_query(elements=cli[Params.ELEMENTS])
            path: str = NIST.get_absolute_path_article(articleId)
            if cli[Params.VERBOSE]:
                print("Chemin local vers le dossier contenant les potentiels: {}".format(path))
            print("OK")
        # Recherche en local
        else:
            print("Récupération des potentiels en local...")
            potentialsId: list[str] = NIST.query_elements(elements=cli[Params.ELEMENTS])
            paths: list[str] = []
            for potentialId in potentialsId:
                paths.extend(NIST.get_absolute_path_potential(potentialId))
            if cli[Params.VERBOSE]:
                print("Chemins locaux:", end="")
                for path in paths:
                    print("\n\t{}".format(path))
            print("OK\n")
        print("####################\n")

    if not cli[Params.NIST_ONLY]:
        # TODO lors du merge avec Kim
        pass