from Inputs import Params


def printArgs(parameters: dict):
    if not parameters[Params.QUIET]:
        print("\n###### Options ######")

        print("Famille d'intéraction: {}".format(parameters[Params.FAMILY]))
        print("Elements: [ {} ]".format(", ".join(parameters[Params.ELEMENTS])))

        if parameters[Params.VERBOSE]:
            print("Mode verbeux")
            if parameters[Params.LOCAL_ONLY]:
                print("Recherche en local seulement")
            elif parameters[Params.REMOTE_ONLY]:
                print("Recherche en ligne seulement")
            else:
                print("Strategie de recherche par défaut")

            if parameters[Params.NIST_ONLY]:
                print("Récupération du NIST uniquement")
            elif parameters[Params.OPENKIM_ONLY]:
                print("Récupération de OpenKIM uniquement")
            else:
                print("Recherche vers toutes les base de données")
            if parameters[Params.LOAD_KIM]:
                print("Téléchargement intégrale de la base de donnée OpenKIM")
            if parameters[Params.LOAD_NIST]:
                print("Téléchargement intégrale de la base de donnée du NIST")

        print("#####################\n")
