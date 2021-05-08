from tkinter import *
from Core import main
from Inputs import Params
from Printers import printArgs


class GUI(Frame):

    def __init__(self, master=Tk()):
        super().__init__(master=master)
        self.master = master

        self.create()

    def create(self):
        self.master.title(
            "IHM_Environnement de développement intelligent pour des simulations numériques de dynamiques moléculaire"
        )
        self.master.geometry("1080x720")
        self.master.minsize(480, 360)
        self.master.config(background='#41B77F')
        self.config(bg='#37827a')

        # Titre de IHM
        label_title = Label(self.master,
                            text=" Formulaire Recherches de molécules", font=("Courrier", 50),
                            bg='#41B77F',
                            fg='white')
        label_title.pack()

        # Champs d'Elements
        label_element = Label(self,
                              text="Element(s) : ",
                              font=("Courrier", 30),
                              bg='#37827a',
                              fg='white')
        label_element.pack()

        indication_element = Label(self,
                                   text="(Veillez séparer chaque élément avec '-')",
                                   font=("Courrier", 15),
                                   bg='#37827a',
                                   fg='red')
        indication_element.pack()

        self._elements = Entry(self,
                               width=100)
        self._elements.insert(0, "Ag-Au-Cu")
        self._elements.pack()

        # Champs d'itération
        label_element = Label(self,
                              text="Famille d'intéraction: ",
                              font=("Courrier", 30),
                              bg='#37827a',
                              fg='white')
        label_element.pack()

        listeFamille = ["eam", "eam/fs", "eam/fs", "meam/c"]
        self._family = StringVar(self)
        self._family.set(listeFamille[0])
        opt = OptionMenu(self,
                         self._family,
                         *listeFamille)
        opt.config(width=70,
                   font=('Helvetica', 20))
        opt.pack(side="top")

        # Champs des Fichiers de traitements
        label_fichier_traitement = Label(self,
                                         text="Type de recherche: ",
                                         font=("Courrier", 30),
                                         bg='#37827a',
                                         fg='white')
        label_fichier_traitement.pack()

        indication_fichier = Label(self,
                                   text="(Il est possible de faire de multiples choix)",
                                   font=("Courrier", 15),
                                   bg='#37827a',
                                   fg='red')
        indication_fichier.pack()

        self._local = BooleanVar(value=True)
        c1 = Checkbutton(self, text="Local", height=2, width=100, font=("Courrier", 12), variable=self._local)
        c1.pack()

        self._remote = BooleanVar(value=True)
        c2 = Checkbutton(self, text="En ligne", height=2, width=100, font=("Courrier", 12), variable=self._remote)
        c2.pack()

        self._nist = BooleanVar(value=True)
        c3 = Checkbutton(self, text="Nist", height=2, width=100, font=("Courrier", 12), variable=self._nist)
        c3.pack()

        self._openkim = BooleanVar(value=False)
        c4 = Checkbutton(self, text="OpenKIM", height=2, width=100, font=("Courrier", 12), variable=self._openkim)
        c4.pack()

        # Button de simulation
        button_simulation = Button(self,
                                   text="Télécharger",
                                   font=("Courrier", 20),
                                   bg='#41B77F',
                                   fg='white',
                                   command=self.send)
        button_simulation.pack()

        self.pack(expand=YES)

    def send(self):

        settings: dict = {
            Params.FAMILY: self._family.get(),
            Params.ELEMENTS: self._elements.get().split('-'),
            Params.QUIET: False,
            Params.VERBOSE: True,
            Params.LOAD_KIM: False,
            Params.LOAD_NIST: False,
            Params.LOCAL_ONLY: (self._local.get() and not self._remote.get()),
            Params.REMOTE_ONLY: (not self._local.get() and self._remote.get()),
            Params.NIST_ONLY: (self._nist.get() and not self._openkim.get()),
            Params.OPENKIM_ONLY: (not self._nist.get() and self._openkim.get()),
        }

        printArgs(settings)
        self.master.destroy()
        main(settings)


if __name__ == "__main__":
    gui: GUI = GUI()
    gui.mainloop()
