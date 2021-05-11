from typing import List
import atomman as am
import shutil
import os
from pathlib import Path

# Vérification que le fichier de base de données est présent
if not os.path.isdir("./potential_LAMMPS"):
    print("Création du dossier de base de donnée Nist")
    os.mkdir("./potential_LAMMPS")


def _clearPotentials(localpath: str = '.'):
    """
    Permet de supprimer tous les articles (dossiers) dans le dossier potential_LAMMPS

    Parametres
    ----------
    localpath : str, optionnel
        Chemin vers un dossier local où les potentiels seront copiés.
        La valeur par défaut est le chemin courant '.'

    Retour
    ----------
    Pas de retour, mais supprime tous les dossiers et fichiers du dossier potential_LAMMPS
    """
    dir = localpath + '/potential_LAMMPS'

    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def downloadAllFamilies() -> set[str]:
    db = am.library.Database(load='lammps_potentials', verbose=False)
    db.load_lammps_potentials()
    return set(db.lammps_potentials_df.pair_style)


def downloadAll(verbose: bool = True, format: str = 'json', localpath: str = '.',
                testException: bool = False, cleanDir: bool = False):
    """
    Permet de télécharger tous les potentiels compatibles LAMMPS de la base du NIST

    Parametres
    ----------
    verbose : bool, optionnel
        Si True, des messages seront affichés pendant l'exécution.
        La valeur par défaut est True.
        Exemple: True ou False
    format : str, optionnel
        Le format des fichiers pour sauver les résultats localement.
        Les valeurs autorisées sont 'xml' et 'json'. La valeur par défaut est 'json'
        Exemple: "json" ou "xml"
    localpath : str, optionnel
        Chemin vers un dossier local où les potentiels seront copiés.
        La valeur par défaut est le chemin courant '.'
    testException : bool, optionnel
        Si True, création d'une erreur (div par 0) pour tester le passage dans l'exception
        False par défaut
        Exemple: True ou False
    cleanDir : bool, optionnel
        Si True, supprime le dossier de téléchargement de tous les potentiels
        Si False, ne supprime pas le dossier de téléchargement
        La valeur par défaut est False.
        Exemple: True ou False

    Temps
    ----------
    Pour télécharger toute la base (test avec 722 potentiels), mode verbose activé, avec clean: environ 10min
    Pour télécharger toute la base (test avec 722 potentiels), sans verbose, avec clean : environ 10min

    Retour
    ----------
    Pas de retour, mais télécharge les potentiels compatible LAMMPS dans le localpath spécifié.
    """

    if cleanDir:
        _clearPotentials()

    # Création de la base de donnée
    lib = am.library.Database(localpath=localpath)
    # Chargement des potentiels LAMMPS du NIST dans la BD local
    lib.load_potentials(verbose=verbose)

    # format des fichiers à importer

    while True:
        try:
            # si on est en mode test de l'except
            if testException:
                # Création d'un exception (div par 0)
                test = 10 * (1 / 0)

            # telechargement des potentiels LAMMPS dans le format choisi
            lib.download_lammps_potentials(format=format, verbose=verbose)
        # Si un problème lors du téléchargement
        except Exception as e:
            print(e)  # Afficher l'erreur

            # Pour tous les fichiers du format téléchargés dans dossier potential_LAMMPS
            for fname in Path(lib.localpath, '../potential_LAMMPS').glob(f'*.{format}'):
                # récupérer que les nom des dossiers des potentiels
                name = fname.stem

                # Passé les potentiels qui ne sont pas LAMMPS
                if name[0] not in ['1', '2']:
                    # les passer
                    continue

                # chemin du dossier dont le nom est passé en paramètre (ex : "potential_LAMMPS")
                dirname = Path(lib.localpath, '../potential_LAMMPS', name)
                # print(dirname)

                # Remove records for potentials without folders to download again
                # Si le chemin ne mêne pas à un dossier
                if not dirname.is_dir():
                    fname.unlink()  # retirer le chemin du path

        else:
            print('finished')
            break


def _getAbsolutePathArticle(id: str = None, localpath: str = ".") -> str:
    """
    Permet de récupérer le chemin absolu d'un article (dossier) qui contient des fichiers de potentiel

    Parametres
    ----------
    id: str
        Une chaîne de caractère qui représente le nom d'un article (dossier)
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Exemple: "1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1"
    localpath : str, optionnel
        Une chaîne de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaîne de caractère, une AssertionError est levée.

    Retour
    ----------
    Une chaîne de caractère qui est le chemin de l'article (dossier) passé en paramètre
    """

    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier, "Il n'y a pas de base de donnée locale"
    assert type(id) == str, "le potentiel doit être un string"
    assert type(localpath) == str, "Le localpath doit être un string"
    ## chargement de la bd local
    try:
        db = am.library.Database(local=True, localpath=localpath, remote=False, load="lammps_potentials")
    except Exception:
        print("Un problème est subvenu avec le chargement de la base de donnée des potentiels")

    ## test de récupération d'un potentiel avec sont id
    ##'1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1'
    potential = db.get_lammps_potential(id=id)
    return os.getcwd() + "/potential_LAMMPS/" + str(potential) + "/"


def downloadOneWithFamilyAndElements(elements: List[str], pair_style: str, localpath: str = ".",
                                     verbose: str = False) -> str:
    """
    Permet de télécharger un article en local en fonction d'une liste d'éléments atomique et d'une famille de pair_style

    Parametres
    ----------
     elements: liste de str
        Une liste de chaîne de caractère qui contient des symboles atomique.
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings de 2 caractères est passé en paramètre, une AssertionError est levée.
        Exemple: ["Ni"] ou ["Ni","C
    pair_style : str
        Un string qui est le pair_style du potentiel à télécharger.
        Exemple: 'eam' ou 'eam/alloy'
    localpath : str, optionnel
        Une chaîne de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaîne de caractère, une AssertionError est levée.

    Retour
    ----------
    l'identifiant de l'article choisit
    """
    assert type(elements) == list, "Les elements doivent passé dans une liste"
    assert len(elements) > 0, "La liste de peut être vide"
    for atom in elements:
        assert type(atom) == str, "Tous les élements de la liste doivents êtres des strings"
        assert len(atom) == 2, "Tous les élements de la liste doivent être sous leur symbole atomique"
    potential = am.load_lammps_potential(pair_style=pair_style, elements=elements, localpath=".", getfiles=True)
    return potential.id


### Test de la fonction downloadOneWithFamilyAndElements
# print(download_potential_element_family(["Ni","Cu"], "eam"))

def downloadAllWithFamilyAndElements(elements: List[str], pair_style: str, verbose: bool = False, localpath: str = ".",
                                     format: str = 'json') -> List[str]:
    """
    Permet de télécharger tous les potentiels compatibles avec la liste d'éléments et la famille passée en paramètre.

    Parametres
    ----------
    elements: liste de str
        Une liste de chaîne de caractère qui contient des symboles atomique.
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings de 2 caractères est passé en paramètre, une AssertionError est levée.
        Exemple: ["Ni"] ou ["Ni","Cu"]
    pair_style : str
        Un string qui est le pair_style du potentiel à télécharger.
        Exemple: 'eam' ou 'eam/alloy'
    localpath : str, optionnel
        Une chaîne de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.

    Temps
    ----------
    Environ 1min30 voir plus avec elements=["Ni","Cu"] et pair_style="eam", pour 3 articles.elements

    Retour
    ----------
    Télécharge les artciles correspondant dans le dossier potential_LAMMPS du localpath, si pas de dossier alors il est créer.
    Si les articles sont déjà présent dans le dossier alors les artciles sont passé et ne sont pas re-téléchargé.
    """
    db = am.library.Database(load='lammps_potentials', verbose=verbose)
    db.load_potentials()
    test = db.get_lammps_potentials(pair_style=pair_style, elements=elements)
    liste_chemin = []
    for article in test:
        liste_chemin.append(_getAbsolutePathArticle(article.id))
    db.save_lammps_potentials(test, format=format, verbose=verbose, localpath=localpath)
    return liste_chemin


### Test de la fonction downloadAllWithFamilyAndElements
# print(downloadAllWithFamilyAndElements(["Ni","Cu"], "eam"))

def queryAllWithFamilyAndElements(elements: List[str], pair_style: str, localpath=".", verbose: bool = False) -> List[
    str]:
    """
    Permet de récupérer les noms des articles LAMMPS qui sont compatibles avec les élements/atomes passés en paramètres

    Parametres
    ----------
    elements: liste de str
        Une liste de chaînes de caractère qui contient des symboles atomique.
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings de 2 caractères est passé en paramètre, une AssertionError est levée.
        Exemple: ["Ni"] ou ["Ni","Cu"]
    pair_style : str
        Un string qui est le pair_style du potentiel à télécharger.
        Exemple: 'eam' ou 'eam/alloy'
    localpath : str, optionnel
        Une chaîne de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaîne de caractère, une AssertionError est levée.

    Temps
    ----------
    Environ 1s voir plus avec elements=["Ni","Cu"] et pair_style="eam", pour 3 articles.

    Retour
    ----------
    Une liste de potentiels qui contient les noms des articles dossiers qui contiennent des potentiels qui correspondent
    au éléments/atomes passés en paramètre

    Pour gérer les potentiels retournés, voir https://www.ctcms.nist.gov/potentials/atomman/tutorial/2.1._Potential_class.html
    """
    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier == True, "Il n'y a pas de base de donnée locale"
    assert type(elements) == list, "Les elements doivent passé dans une liste"
    assert len(elements) > 0, "La liste de peut être vide"
    assert type(localpath) == str, "Le localpath doit être un string"
    for atom in elements:
        assert type(atom) == str, "Tous les élements de la liste doivents êtres des strings"
        # assert len(atom) == 2, "Tous les élements de la liste doivent être sous leur symbole atomique"

    try:
        db = am.library.Database(local=True, localpath=localpath, remote=False, verbose=verbose,
                                 load="lammps_potentials")
    except Exception:
        print("Un problème est subvenu avec le chargement de la base de donnée des potentiels")

    potentials = db.get_lammps_potentials(elements=elements, pair_style=pair_style)
    cpt = 0
    liste_correspondance = []
    for potential in potentials:
        ## n'afficher que les dossiers non vide (ne pas afficher les dossier OpenKim)
        if potential.id[0] in ['1', '2']:
            liste_correspondance.append(_getAbsolutePathArticle(potential.id))
            cpt += 1
    print("Il y a " + str(cpt) + " correspondances")
    return liste_correspondance

### Test de la fonction
# print(test(["Ni", "Cu"], "eam"))
