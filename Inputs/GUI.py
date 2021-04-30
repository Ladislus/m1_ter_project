from tkinter import *
from tkinter import messagebox

# DECLARATION
# --------------------------------------------------------------------------------------------
from tkinter.ttk import Combobox

listeFamille = ["eam", "eam/fs", "eam/fs", "meam/c"]
file_de_trait = []
select_iteration = "null"
elements = "null"


# FONCTIONS
# --------------------------------------------------------------------------------------------
def getElementEntry():
    elt = element.get()
    return elt


def callback(*args):
    labelTest.configure(text="La famille d'itération selectionnée est {}".format(variable.get()))


def getFamilleIterationEntry():
    familleIter = variable.get()
    return familleIter


def getFichier():
    if (var1.get() == 1):
        return "Local"
    if (var2.get() == 1):
        return "Nist"
    if (var3.get() == 1):
        return "OpenKim"
    else:
        return "Auncun fichier à été sélectionné !"


def formulaireEnvoyer():
    messagebox.showinfo("Affirmez-vous ces informations?", getElementEntry())
    messagebox.showinfo("Affirmez-vous ces informations?", getFamilleIterationEntry())
    messagebox.showinfo("Affirmez-vous ces informations?", getFichier())


# ---------------------------------------------------------------------------------------------
# Personaliser La fenetre principale
fenetrePrincipale = Tk()
# ------------------------------------------------------------------------------------------------------------
fenetrePrincipale.title(
    "IHM_Environnement de développement intelligent pour des simulations numériques de dynamiques moléculaire")
fenetrePrincipale.geometry("1080x720")
fenetrePrincipale.minsize(480, 360)
fenetrePrincipale.config(background='#41B77F')

# Creer la frame
frame = Frame(fenetrePrincipale, bg='#37827a')

# Titre de IHM
label_title = Label(fenetrePrincipale, text=" Formulaire Recherches de molécules", font=("Courrier", 50), bg='#41B77F',
                    fg='white')
label_title.pack()

# FORMULAIRE
# ---------------------------------------------------------------------------------------------------------
# Champs d'Elements
label_element = Label(frame, text="Element(s) : ", font=("Courrier", 30), bg='#37827a', fg='white')
label_element.pack()
indication_element = Label(frame, text="(Veillez séparer chaque élément avec '-')", font=("Courrier", 15), bg='#37827a',
                           fg='red')
indication_element.pack()

element = Entry(frame, width=100, )
element.insert(0, "Ag-Au-Cu")
element.pack()

# -------------------------------------------------------------------------------------------------------------
# Champs d'itération
label_element = Label(frame, text="Famille d'itération: ", font=("Courrier", 30), bg='#37827a', fg='white')
label_element.pack()
variable = StringVar(frame)
variable.set(listeFamille[0])
opt = OptionMenu(frame, variable, *listeFamille)
opt.config(width=70, font=('Helvetica', 20))
opt.pack(side="top")

labelTest = Label(text="", font=('Helvetica', 20), fg='red')
labelTest.pack(side="top")

variable.trace("w", callback)

# -------------------------------------------------------------------------------------------------------------
# Champs des Fichiers de traitements
label_fichier_traitement = Label(frame, text="Fichiers de traitement: ", font=("Courrier", 30), bg='#37827a',
                                 fg='white')
label_fichier_traitement.pack()
indication_fichier = Label(frame, text="(Il est possible de faire de multiples choix)", font=("Courrier", 15),
                           bg='#37827a', fg='red')
indication_fichier.pack()

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
c1 = Checkbutton(frame, text="Local", height=2, width=100, font=("Courrier", 12), variable=var1)
c2 = Checkbutton(frame, text="Nist", height=2, width=100, font=("Courrier", 12), variable=var2)
c3 = Checkbutton(frame, text="OpenKim", height=2, width=100, font=("Courrier", 12), variable=var3)
c1.pack()
c2.pack()
c3.pack()

# -------------------------------------------------------------------------------------------------------------
# Button de simulation

button_simulation = Button(frame, text="Simulation", font=("Courrier", 20), bg='#41B77F', fg='white',
                           command=formulaireEnvoyer)
button_simulation.pack()

frame.pack(expand=YES)
