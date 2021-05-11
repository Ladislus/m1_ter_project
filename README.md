# Master 1 : Projet TER

## Collaborateurs

Étudiants:
 - BAYOUSSOULA Habib
 - RIBARDIÈRE Tom
 - SAJOT Nathan
 - VADET Alexandre
 - WALCAK Ladislas

Encadrants:
 - ROBERT Sophie
 - BRAULT Pascal

## Requirements

### Python 3.9  
Installation Ubuntu `sudo apt install python3.9`
   
### Les packages `Atomman`, `Tkinter` et `Argparse`  
Pour installer ces packages, vous pouvez utiliser le fichier requirements.txt:  
`pip install -r requirements.txt`  

Nous conseillons d'utiliser un virtualenv, afin de ne pas encombrer votre installation de python global  
```bash
# virtualenv -p [version de python] [nom du dossier virtualenv]
# Par exemple
virtualenv -p python3.9 venv
# activation du venv
source venv/bin/activate
#installation des packages dans le venv
pip install -r requirements.txt 
```
Afin de desactiver le venv, exécutez `deactivate`  

Attention: Il est possible que lors de l'installation des packages sur Ubuntu, l'erreur suivant se produise:  
`#include Python.h : No such file or directory`
Pour cela, il faut installer les headers python (mettre la vesion de python qui correspond):  
`sudo apt install python3.9-dev`

## Utilisation

### Version CLI
Afin de lancer la version CLI de l'application, écecuter:  
`python3.9 Core.py [Options...] Famille Elements...`

avec:  
 - `Famille`: La famille d'intéraction  
   ex: "eam", "meam/c", ...  
   
 - `Elements...`: La liste des éléments qui doivent intéragir, séparé par des espaces  
   ex: "Ni Ci Ag", "Ag Au Cu", ...
   
 - `[Options...]`: *Optionnel*, la liste des options d'éxécution parmi:
    - --verbose, -v: Active la version verbeuse, qui  affiche plus d'information  
      ou
    - --quiet, -q: Active la version silencieuse, qui désactive la plupart des affichages
    
    - --local-only, -l: Effectue des recherche sur les bases de données locales uniquement  
      ou
    - --remote-only, -r: Effectue des recherches sur les bases de données distantes uniquement
    
    - --openkim-only, -k: Effectue des recherches sur la base de données distante d'OpenKIM uniquement  
    Attention: Ne fonctionne pas avec l'option --local-only  
      ou
    - --nist-only, -n: Effectue des recherches sur la base de données distante du NIST uniquement  
    Attention: Ne fonctionne pas avec l'option --local-only
    
    - --force-nist, -fn: Avant toutes requêtes, télécharge en local l'intégralité de la base de données NIST, compatible avec LAMMPS
    - --force-kim, -fk: Avant toutes requêtes, télécharge en local l'intégralité de la base de données OpenKIM, compatible avec LAMMPS

### Version GUI
Afin de lancer la version graphique de l'application, éxecuter:  
`python3.9 GUI.py`

## Architecture de l'application

### [Databases](./Databases)
Ce package contient l'intégralitée des fonctions d'appel vers les bases de données distantes.
Ce package, combiné avec les Handlers, permet de créer un sniffeur pour une base de données donnée.

### [Handler](./Handlers)
Ce package contient la logique des appels vers les bases de données distantes.
Il prend en argument la liste des options de recherche, et effectue les bons appels, dans le bon ordre.
Ce package, combiné avec les Databases, permet de créer un sniffeur pour une base de données donnée.

### [Inputs](./Inputs)
Ce package contient l'intégralitée des éléments permettant l'utilisation du CLI.

### [Printers](./Printers)
Ce package contient des fonctions d'affichage, permettant de généraliser les méthodes d'affichage, et produire un affichage homogène.