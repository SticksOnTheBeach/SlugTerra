from back_perso import *
from tkinter import *
from tkinter import messagebox


class ChoixPerso(Frame):

    def __init__(self, master, equipe: Equipe):
        super().__init__(master)
        self.equipe = equipe
        self.charger_images()
        self.creer_widgets()
        self.placer_widgets()

    def charger_images(self):

        self.images = {}
        for perso in self.equipe.tab:
            self.images[perso.couche1_id] = PhotoImage(file=perso.icon)

    def creer_widgets(self):

        self.widgets = []
        self.frame_spells = Frame(self)
        for perso in self.equipe.tab:
            btn_select = Button(self, text=perso.nom_carte, bg="red", fg="white", compound=BOTTOM,
                                image=self.images[perso.couche1_id],
                                command=lambda p=perso: self.on_btn_perso_click(p))
            self.widgets.append(btn_select)
            self.creer_widgets_sorts(perso)

    def creer_widgets_sorts(self, perso):

        for spell in perso.grimoire:
            btn_spell = Button(self.frame_spells, text=spell["nom"], bg="blue", fg="white",
                               command=lambda p=perso, s=spell["nom"]: self.on_btn_spell_click(p, s))
            btn_spell.pack(side=LEFT, padx=5, pady=5)

    def placer_widgets(self):

        for i, btn in enumerate(self.widgets):
            btn.grid(row=i, column=1, padx=10, pady=10)
        self.frame_spells.grid(row=0, column=2, padx=10, pady=10)

    def on_btn_perso_click(self, perso):

        messagebox.showinfo("Personnage Sélectionné", f"Nom : {perso.nom_carte}\nID : {perso.couche1_id}")

    def on_btn_spell_click(self, perso, spell_name):

        result = perso.lancer_sort(spell_name)
        messagebox.showinfo("Sort Lancé", result)



if __name__ == "__main__":

    equipe = Equipe()

    perso1 = Perso("CHARA_RAMMSTONE")
    perso2 = Perso("CHARA_ENIGMO")
    perso3 = Perso("CHARA_INFURNUS")
    equipe.ajouter(perso1)
    equipe.ajouter(perso2)
    equipe.ajouter(perso3)
    print(equipe)

    app = Tk()
    frm = ChoixPerso(app, equipe)
    frm.grid()
    app.mainloop()