from tkinter import *
from Core import main


class GUI(Frame):

    def __init__(self, master=Tk()):
        super().__init__(master=master)
        self.master = master
        self.pack()

        self.create()

    def create(self):
        self.master.title(
            "IHM_Environnement de développement intelligent pour des simulations numériques de dynamiques moléculaire"
        )
        self.master.geometry("1080x720")
        self.master.minsize(480, 360)
        self.master.config(background='#41B77F')

        # Creer la frame
        frame = Frame(self.master, bg='#37827a')

        # Titre de IHM
        label_title = Label(self.master, text=" Formulaire Recherches de molécules", font=("Courrier", 50),
                            bg='#41B77F',
                            fg='white')
        label_title.pack()

        # Champs d'Elements
        label_element = Label(frame,
                              text="Element(s) : ",
                              font=("Courrier", 30),
                              bg='#37827a',
                              fg='white')
        label_element.pack()

        indication_element = Label(frame,
                                   text="(Veillez séparer chaque élément avec '-')",
                                   font=("Courrier", 15),
                                   bg='#37827a',
                                   fg='red')
        indication_element.pack()

        element = Entry(frame, width=100, )
        element.insert(0, "Ag-Au-Cu")
        element.pack()

        # Champs d'itération
        label_element = Label(frame,
                              text="Famille d'itération: ",
                              font=("Courrier", 30),
                              bg='#37827a',
                              fg='white')
        label_element.pack()

        listeFamille = ["eam", "eam/fs", "eam/fs", "meam/c"]
        variable = StringVar(frame)
        variable.set(listeFamille[0])
        opt = OptionMenu(frame,
                         variable,
                         *listeFamille)
        opt.config(width=70,
                   font=('Helvetica', 20))
        opt.pack(side="top")

        labelTest = Label(text="",
                          font=('Helvetica', 20),
                          fg='red')
        labelTest.pack(side="top")

        variable.trace("w", self.callback)

        # Champs des Fichiers de traitements
        label_fichier_traitement = Label(frame,
                                         text="Fichiers de traitement: ",
                                         font=("Courrier", 30),
                                         bg='#37827a',
                                         fg='white')
        label_fichier_traitement.pack()

        indication_fichier = Label(frame,
                                   text="(Il est possible de faire de multiples choix)",
                                   font=("Courrier", 15),
                                   bg='#37827a',
                                   fg='red')
        indication_fichier.pack()

        var1 = IntVar()
        c1 = Checkbutton(frame, text="Local", height=2, width=100, font=("Courrier", 12), variable=var1)
        c1.pack()

        var2 = IntVar()
        c2 = Checkbutton(frame, text="Nist", height=2, width=100, font=("Courrier", 12), variable=var2)
        c2.pack()

        var3 = IntVar()
        c3 = Checkbutton(frame, text="OpenKim", height=2, width=100, font=("Courrier", 12), variable=var3)
        c3.pack()

        # Button de simulation
        button_simulation = Button(frame,
                                   text="Simulation",
                                   font=("Courrier", 20),
                                   bg='#41B77F',
                                   fg='white',
                                   command=self.send)
        button_simulation.pack()
        frame.pack(expand=YES)

    def callback(self):
        pass

    def send(self):
        # TODO Recupérer infos
        main()


if __name__ == "__main__":
    gui: GUI = GUI()
    gui.mainloop()
