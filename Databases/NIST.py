from typing import List
import atomman as am
import shutil
import os
from os.path import isfile, join
from pathlib import Path


def cleanDirPotential(localpath: str = '.'):
    """
    Permet de supprimer tous les articles (dossiers) dans le dossier potential_LAMMPS

     Parametres
    ----------
    localpath : str, optionel
        Chemin vers un dossier local où les potentiels seront copiés.
        La valeur par défaut est le dossier ou est lancé le '.'
    """
    dir = localpath + '/potential_LAMMPS'

    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def getAllPairStyles() -> set[str]:
    db = am.library.Database(load='lammps_potentials', verbose=False)
    db.load_lammps_potentials()
    return set(db.lammps_potentials_df.pair_style)


def downloadAll(verbose: bool = True, format: str = 'json', localpath: str = '.',
                testException: bool = False, cleanDir: bool = False):
    """
    Permet de télécharger tous les potentiels compatibles LAMMPS de la base du NIST

    Parametres
    ----------
    verbose : bool, optionel
        Si True, des messages seront affichés pendant l'éxécution.
        La valeur par défaut est True.
        Exemple: True ou False
    format : str, optionel
        Le format des fichiers pour sauver les résulats localement.
        Les valeurs autorisées sont 'xml' et 'json'. La valeur par défaut est 'json'
        Exemple: "json" ou "xml"
    localpath : str, optionel
        Chemin vers un dossier local où les potentiels seront copiés.
        La valeur par défaut est le dossier ou est lancé le '.'
    testException : bool, optionel
        Si True, création d'une erreur (div par 0) pour tester le passage dans l'exception
        False par defaut
        Exemple: True ou False
    cleanDir : bool, optionel
        Si True, supprime le dossier de téléchargement de tous les potentiels
        Si False, ne supprime pas le dossier de téléchargement
        La valeur par défaut est False.
        Exemple: True ou False

    Temps
    ----------
    Pour télécharger toutes la base (test avec 722 potentiels), mode verbose activé, avec clean: environ 10min
    Pour télécharger toutes la base (test avec 722 potentiels), sans verbose, avec clean : environ 10min
    """

    if cleanDir:
        cleanDirPotential()

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


# download_all_lammps_potentials()

def download_lammps_pair_style(pair_style: List[str], verbose: bool = True, localpath: str = ".", format: str = 'json'):
    """
    Permet de télécharger des potentiels compatibles LAMMPS de la base du NIST, en fonction d'une liste de pair_style

    Parametres
    ----------
    format : str, optionel
        Le format des fichiers pour sauver les résulats localement.
        Les valeurs autorisées sont 'xml' et 'json'. La valeur par défaut est 'json'
        Exemple "json" ou "xml"
    pair_style : [str]
        Une liste de string qui sont les pair_style des potentiels à télécharger.
        Exemple: ['eam','eam/alloy','eam/fs/alloy','meam/c']
    verbose : bool, optionel
        Si True, des messages seront affichés pendant l'éxécution.
        La valeur par défaut est True.
        Exemple: True ou False
    localpath : str, optionel
        Chemin vers un dossier local où les potentiels seront copiés.
        La valeur par défaut est le dossier ou est lancé le .
    Temps
    ----------
    Pour télécharger les potentiels des familles eam, eam/alloy, eam/fs/alloy, meam/c :
    108 potentiels :
    """
    assert type(pair_style) == list, "Les elements doivent passé dans une liste"
    assert len(pair_style) > 0, "La liste de peut être vide"
    for pair in pair_style:
        assert type(pair) == str, "Tous les élements de la liste doivents êtres des strings"

    db = am.library.Database(load='lammps_potentials', verbose=verbose)
    db.load_potentials()
    ### NE TROUVE PAS LE PAIR_STYLE MEAM/C
    # all_pair_styles = np.unique(db.lammps_potentials_df.pair_style)
    # print(all_pair_styles)
    # for pair in pair_style:
    #     assert pair in all_pair_styles, pair+" doit être dans un pair_style compatible LAMMPS"
    test = db.get_lammps_potentials(pair_style=pair_style)
    db.save_lammps_potentials(test, format=format, verbose=verbose, localpath=localpath)


# download_lammps_pair_style(['eam','eam/alloy','eam/fs','meam/c']) #-> fonctionne
# download_lammps_pair_style([]) #-> AssertionError: La liste de peut être vide
# download_lammps_pair_style(["bonjour"]) #-> fonctionne alors que non
# download_lammps_pair_style(1) #-> AssertionError: Les elements doivent passé dans une liste

def download_lammps_query(pot_id: str = None, id: str = None, elements: List[str] = None) -> str:
    """
    Permet de télécharger un article (dossier) qui contient des fichiers potentiels avec le pot_id de l'article, l'identifiant de l'article
    ou avec une liste d'éléments (symbole atomique de 2 caractères).
    Au moins, un des paramètres doit être donné.

    Parametres
    ----------
    pot_id : str, optionel
        Une chaine de caractère qui représente l'identifiant d'un potentiel.
        Si une liste d'identifiant est passé alors un menu vous demandera de choisir
        lequel des 2 vous voulez télécharger
        exemple : 2009--Bonny-G-Pasianot-R-C-Castin-N-Malerba-L--Fe-Cu-Ni
    id : str, optionel
        Une chaine de caractère qui représente l'identifiant de l'objet qui représente un potentiel.
        C'est le nom du dossier qui sera télécharger (également le nom de l'article qui contient les fichiers potentiels)
        Si une liste d'identifiant est passé alors un menu vous demandera de choisir
        lequel des 2 vous voulez télécharger
        exemple : 2009--Bonny-G--Fe-Cu-Ni--LAMMPS--ipr1
    elements: str, liste de str, optionnel
        Une chaine de cractère ou une liste de caractère qui représente les éléments que doit utiliser
        le potentiel. Si plusieurs potentiels correspondent aux éléments alors, un menu vous demandera lequel
        vous voulez télécharger.
        Exemple: ["Ni","Cu"]
    Temps
    ----------
    Pas de temps spécifique car s'il y a plusieurs correspondance alors vous aurez un menu qui vous demande de
    choisir le potentiel que vous voule, ce qui ruine donc la mesure du temps.

     Retour
    ----------
    Vous retournera l'id (nom du dossier) que vous aurez téléchargé.
    """
    # try:
    if (pot_id is not None and (id is None and elements is None)):
        assert type(pot_id) == str, "le paramètre pot_id doit être un string"
        potential = am.load_lammps_potential(potid=pot_id, getfiles=True)
    if (id is not None and (pot_id is None and elements is None)):
        assert type(id) == str, "le paramètre id doit être un string"
        potential = am.load_lammps_potential(id=id, getfiles=True)
    if (elements is not None and (id is None and pot_id is None)):
        assert type(elements) == list, "Les elements doivent passé dans une liste"
        assert len(elements) > 0, "La liste de peut être vide"
        for atom in elements:
            assert type(atom) == str, "Tous les élements de la liste doivents êtres des strings"
            assert len(atom) == 2, "Tous les élements de la liste doivent être sous leur symbole atomique"
        potential = am.load_lammps_potential(elements=elements, localpath=".", getfiles=True)
    # except Exception:
    # return "il y a une erreur dans les arguments de la fonction"
    return potential.id


## Test de la fonction download_lammps_query
# print(download_lammps_query(elements=["Ni","Fe"])) #-> fonctionne
# print(download_lammps_query(elements=["Nickel","Fer"])) #-> AssertionError: Tous les élements de la liste doivent être sous leur symbole atomique
# print(download_lammps_query(elements="Nickel")) #-> AssertionError: Les elements doivent passé dans une liste
# print(download_lammps_query(elements=1)) #-> AssertionError: Les elements doivent passé dans une liste
# print(download_lammps_query(elements=[])) #-> AssertionError: La liste de peut être vide
# print(download_lammps_query(elements=[1])) #-> AssertionError: Tous les élements de la liste doivents êtres des strings
# print(download_lammps_query(elements=[1,12])) #-> AssertionError: Tous les élements de la liste doivents êtres des strings

# print(download_lammps_query(pot_id="2009--Bonny-G-Pasianot-R-C-Castin-N-Malerba-L--Fe-Cu-Ni")) # -> fonctionne
# print(download_lammps_query(pot_id="bonjour")) # -> ValueError: No matching LAMMPS potentials found
# print(download_lammps_query(pot_id=[])) # -> AssertionError: le paramètre pot_id doit être un string
# print(download_lammps_query(pot_id=["test"])) # -> AssertionError: le paramètre pot_id doit être un string
# print(download_lammps_query(pot_id=[1])) # -> AssertionError: le paramètre pot_id doit être un string
# print(download_lammps_query(pot_id=1)) # -> AssertionError: le paramètre pot_id doit être un string

# print(download_lammps_query(id="2009--Bonny-G--Fe-Cu-Ni--LAMMPS--ipr1")) # -> fonctionne
# print(download_lammps_query(id="bonjour")) # -> ValueError: No matching LAMMPS potentials found
# print(download_lammps_query(id=1)) # -> AssertionError: le paramètre id doit être un string
# print(download_lammps_query(id=[])) # -> AssertionError: le paramètre id doit être un string
# print(download_lammps_query(id=[1])) # -> AssertionError: le paramètre id doit être un string
# print(download_lammps_query(id=["bonjour"])) # -> AssertionError: le paramètre id doit être un string

def get_potentials_number(localpath: str = ".") -> None:
    """
    Permet de récupérer le nombre de potentiels compatible LAMMPS et OpenKim de la base de donnée locale
    Les potentiels OpenKim de la base ne sont que des dossiers vides donc, il ne sont pas utilisables

    Parametres
    ----------
    localpath : str, optionel
        Une chaine de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaine de caractère, une AssertionError est levée

    Retour
    ----------
    Pas de retour, que des prints (affichage)
    """
    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier == True, "Il n'y a pas de base de donnée locale"
    assert type(localpath) == str, "Le localpath doit être un string"
    db = am.library.Database(local=True, localpath=localpath, remote=False, load="lammps_potentials")
    cpt_lammps = 0
    cpt_OpenKim = 0
    if db.lammps_potentials is not None:
        for potential in db.get_lammps_potentials():
            if potential.id[0] in ['1', '2']:
                cpt_lammps += 1
            else:
                cpt_OpenKim += 1
    print("Il y a " + str(cpt_lammps) + " potentiels compatibles LAMMPS dans la base de donnée locale")
    print("Il y a " + str(cpt_OpenKim) + " potentiels OpenKim dans la base de donnée locale")


## Test de la fonction get_potentials_numbers
# get_potentials_number() ##-> fonctionne

## Sans le dossier potential_LAMMPS (BD)
# get_potentials_number() ## -> AssertionError: Il n'y a pas de base de donnée locale

## Avec le dossier potential_LAMMPS (BD) vide##############""
# get_potentials_number() ## -> Il y a 0 potentiels compatibles LAMMPS dans la base de donnée locale
#####################################

def get_absolute_path_article(pot_id: str = None, localpath: str = ".") -> str:
    """
    Permet de récupérer le chemin absolu d'un article (dossier) qui contient des fichiers de potentiel

    Parametres
    ----------
    pot_id: str
        Une chaine de caractère qui représente le nom d'un article (dossier)
        Si un autre type est passé en paramètre, un AssertionError est levée.
        Exemple: "1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1"
    localpath : str, optionel
        Une chaine de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaine de caractère, une AssertionError est levée.

    Retour
    ----------
    Une chaine de caractère qui est le chemin de l'article (dossier) passé en paramètre

    """
    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier == True, "Il n'y a pas de base de donnée locale"
    assert type(pot_id) == str, "le potentiel doit être un string"
    assert type(localpath) == str, "Le localpath doit être un string"
    ## chargement de la bd local
    try:
        db = am.library.Database(local=True, localpath=localpath, remote=False, load="lammps_potentials")
    except Exception:
        print("Un problème est subvenu avec le chargement de la base de donnée des potentiels")

    ## test de récupération d'un potentiel avec sont id
    ##'1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1'
    potential = db.get_lammps_potential(id=pot_id)
    return os.getcwd() + "/potential_LAMMPS/" + str(potential) + "/"


## Test de la fonction get_absolute_path_article

# print(get_absolute_path_article("1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1")) ## -> fonctionne
# print(get_absolute_path_article("bonjour")) ## -> ValueError: No matching LAMMPS potentials found
# print(get_absolute_path_article(1)) ## -> AssertionError: le potentiel doit être un string
# print(get_absolute_path_article([])) ## -> AssertionError: le potentiel doit être un string

def get_absolute_path_potential(pot_id: str = None, localpath=".") -> List[str]:
    """
    Permet de récupérer le chemin absolu des fichiers potentiels d'un article (dossier) passé en paramètre

    Parametres
    ----------
    pot_id: str
        Une chaine de caractère qui représente le nom d'un article (dossier)
        Si un autre type est passé en paramètre, un AssertionError est levée.
        Exemple : "1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1"
    localpath : str, optionel
        Une chaine de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaine de caractère, une AssertionError est levée.

    Retour
    ----------
    Une liste de chaine de caractère qui contient les chemins des fichier de l'article (dossier) passé en paramètre

    """
    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier == True, "Il n'y a pas de base de donnée locale"
    assert type(pot_id) == str, "le potentiel doit être un string"
    assert type(localpath) == str, "Le localpath doit être un string"
    ## chargement de la bd local
    try:
        db = am.library.Database(local=True, localpath=localpath, remote=False, load="lammps_potentials")
    except Exception:
        print("Un problème est subvenu avec le chargement de la base de donnée des potentiels")
    ## test de récupération d'un potentiel avec sont id
    ##'1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1'
    potential = db.get_lammps_potential(id=pot_id)

    mypath = localpath + "/potential_LAMMPS/" + str(potential) + "/"
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    liste_file = []
    for file in onlyfiles:
        liste_file.append(os.getcwd() + "/potential_LAMMPS/" + str(potential) + "/" + str(file))
    # for file in liste_file:
    #     print(file)
    return liste_file


### Tests sur la fonction get_absolute_path_potential

# print(get_absolute_path_potential("1985--Foiles-S-M--Ni-Cu--LAMMPS--ipr1")) ## -> fonctionne
# print(get_absolute_path_potential(1)) ## -> AssertionError: le potentiel doit être un string
# print(get_absolute_path_potential([])) ## -> AssertionError: le potentiel doit être un string
# print(get_absolute_path_potential("bonjour")) ## -> ValueError: No matching LAMMPS potentials found


def query_elements(elements: List[str], localpath=".") -> List[str]:
    """
    Permet de récupérer les noms des articles LAMMPS qui sont compatibles avec les élements/atomes passés en paramètres

    Parametres
    ----------
    elements: liste de str
        Une liste de chaine de caractère qui contient des symboles atomique.
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings de 2 caractères est passé en paramètre, une AssertionError est levée.
        Exemple: ["Ni"] ou ["Ni","Cu"]
    localpath : str, optionel
        Une chaine de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaine de caractère, une AssertionError est levée.

    Retour
    ----------
    Une liste de chaine de potentiels qui contient les noms des articles dossiers qui contiennent des potentiels qui correspondent
    au éléments/atomes passé en paramètre

    Pour gérer les potentiels retournés, voir https://www.ctcms.nist.gov/potentials/atomman/tutorial/2.1._Potential_class.html
    """
    db_dossier = os.path.isdir(localpath + "/potential_LAMMPS")

    assert db_dossier == True, "Il n'y a pas de base de donnée locale"
    assert type(elements) == list, "Les elements doivent passé dans une liste"
    assert len(elements) > 0, "La liste de peut être vide"
    assert type(localpath) == str, "Le localpath doit être un string"
    for atom in elements:
        assert type(atom) == str, "Tous les élements de la liste doivents êtres des strings"
        assert len(atom) == 2, "Tous les élements de la liste doivent être sous leur symbole atomique"

    try:
        db = am.library.Database(local=True, localpath=localpath, remote=False, load="lammps_potentials")
    except Exception:
        print("Un problème est subvenu avec le chargement de la base de donnée des potentiels")

    potentials = db.get_lammps_potentials(elements=elements)
    cpt = 0
    liste_correspondance = []
    for potential in potentials:
        ## n'afficher que les dossiers non vide (ne pas afficher les dossier OpenKim)
        if potential.id[0] in ['1', '2']:
            # print(potential.potid)
            liste_correspondance.append(potential)
            cpt += 1
    # print("Il y a " + str(cpt) + " correspondances")
    return liste_correspondance

### Test de la fonction query_elements
# print(query_elements(elements=["Ni"])) ## -> fonctionne
# print(query_elements(elements=[1])) ## -> AssertionError Tous les élements de la liste doivents êtres des strings
# print(query_elements(elements=[1,2,3,4,"test"])) ## -> AssertionError Tous les élements de la liste doivents êtres des strings
# print(query_elements(elements=["test",1,2,3,4])) ## -> AssertionError Tous les élements de la liste doivent être sous leur symbole atomique
# print(query_elements(elements=["Ni",1,2,3,4])) ## -> AssertionError Tous les élements de la liste doivents êtres des strings
# print(query_elements(elements=[])) ## -> AssertionError La liste de peut être vide
# print(query_elements(elements="Ni")) ## -> AssertionError Les elements doivent passé dans une liste
# print(query_elements(elements=1)) ## -> AssertionError Les elements doivent passé dans une liste
# print(query_elements(elements=["Nickel","Cuivre"])) ## -> AssertionError Tous les élements de la liste doivent être sous leur symbole atomique

def downloadOneWithFamilyAndElements(elements: List[str], pair_style: str, localpath:str = ".", verbose:str=False) -> str:
    """
    Permet de télécharger un article en local en fonction d'une liste d'élements atomique et d'une famille de pair_style

    Parametres
    ----------
     elements: liste de str
        Une liste de chaine de caractère qui contient des symboles atomique.
        Si un autre type est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings est passé en paramètre, une AssertionError est levée.
        Si une liste qui ne contient pas que des strings de 2 caractères est passé en paramètre, une AssertionError est levée.
        Exemple: ["Ni"] ou ["Ni","Cu"]
    localpath : str, optionel
        Une chaine de caractère qui représente le chemin vers le dossier potential_LAMMPS.
        Par défaut, le chemin est le chemin courant.
        Si l'utilisateur passe autre chose qu'une chaine de caractère, une AssertionError est levée.
    pair_style : str
        Un string qui est le pair_style du potentiel à télécharger.
        Exemple: 'eam' ou 'eam/alloy'
    Retour
    ----------
    l'identifiant de l'article choisit
    """
    assert type(elements) == list, "Les elements doivent passé dans une liste"
    assert len(elements) > 0 , "La liste de peut être vide"
    for atom in elements:
        assert type(atom) == str, "Tous les élements de la liste doivents êtres des strings"
        assert len(atom) == 2,"Tous les élements de la liste doivent être sous leur symbole atomique"
    potential = am.load_lammps_potential(pair_style=pair_style, elements=elements,localpath=".",getfiles=True)
    return potential.id

### Test de la fonction download_potential_element_family
#print(download_potential_element_family(["Ni","Cu"], "eam"))

