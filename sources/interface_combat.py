import json
import tkinter as tk
from tkinter import *
from back_perso import Perso
from tkinter.messagebox import showinfo, showwarning
from back_game import *
from tkinter import Listbox, Label, Frame, PhotoImage


def charger_tout_les_characters():
    fichier = open(file="datas/data_characters.json", mode="r")
    mesDonnees = json.load(fichier)
    fichier.close()
    return mesDonnees

class RoundedButton(Canvas):
    def __init__(self, master, text, command, radius=20, width=100, height=40, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.radius = radius

        self.bg_color = kwargs.get("bg", "grey")
        self.creer_rectangle_arrondie(2, 2, width - 2, height - 2, fill=self.bg_color, outline="", tags="button")
        self.create_text(width / 2, height / 2, text=text, tags="text", fill="white")

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def creer_rectangle_arrondie(self, x1, y1, x2, y2, **kwargs):
        points = [x1 + self.radius, y1,
                  x2 - self.radius, y1,
                  x2, y1,
                  x2, y1 + self.radius,
                  x2, y2 - self.radius,
                  x2, y2,
                  x2 - self.radius, y2,
                  x1 + self.radius, y2,
                  x1, y2,
                  x1, y2 - self.radius,
                  x1, y1 + self.radius,
                  x1, y1]
        if "outline" in kwargs:
            kwargs["outline"] = kwargs.get("fill", self.bg_color)
        else:
            kwargs["outline"] = kwargs.get("fill", self.bg_color)

        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_press(self, event):
        self.itemconfig("button", fill="darkgrey")

    def _on_release(self, event):
        self.itemconfig("button", fill=self.bg_color)
        if event.x > 0 and event.x < self.winfo_width() and event.y > 0 and event.y < self.winfo_height():
            self.command()

    def _on_enter(self, event):
        self.itemconfig("button", fill="lightgrey")

    def _on_leave(self, event):
        self.itemconfig("button", fill=self.bg_color)

class InterfaceCombat(Toplevel):
    def __init__(self, master, personnage_jouable: Perso, personnage_ennemi: Perso, game : Game):
        super().__init__(master)
        self.personnage_jouable = personnage_jouable
        self.personnage_ennemi = personnage_ennemi

        master.grab_set()
        self.grab_set()

        self.game = game
        # Supprimer les boutons de la fenêtre (fermer, réduire, etc.)
        self.overrideredirect(True)

        self.charger_images()
        self.creer_widgets()
        self.placer_widgets()
        self.combat_termine = False

        self.centrer_fenetre()


    def centrer_fenetre(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        master_x = self.master.winfo_rootx()
        master_y = self.master.winfo_rooty()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()


        x = master_x + (master_width - width) // 2
        y = master_y + (master_height- height) // 2
        self.geometry(f"+{x}+{y}")


    def charger_images(self):
        self.image_jouable = tk.PhotoImage(file=self.personnage_jouable.icon)
        self.image_enemi = tk.PhotoImage(file=self.personnage_ennemi.icon)

    def creer_widgets1(self):
        self.label_jouable = tk.Label(self,
                                      image=self.image_jouable,
                                      text=self.personnage_jouable,
                                      compound=tk.TOP)
        self.label_enemi = tk.Label(self,
                                    image=self.image_enemi,
                                    text=self.personnage_ennemi,
                                    compound=tk.TOP)
        self.msg_info = f"Vous rencontrez un {self.personnage_ennemi.nom}"
        self.label_info = tk.Label(self, text=self.msg_info)
        self.bouton_attaquer = tk.Button(self, text="Attaquer", command=self.on_btn_attaquer_click)
        self.bouton_magie = tk.Button(self, text="Magie", command=self.on_btn_magie_click)
        self.bouton_changer_slug = tk.Button(self, text="Changer Slug", command=self.on_btn_choisir_slug_click)
        self.bouton_fuir = tk.Button(self, text="Fuir", command=self.on_btn_fuir_click)

    def creer_widgets(self):
        inv_frame = LabelFrame(self, text="Objets à vendre", bg="black", fg="white")
        inv_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        items_frame = Frame(inv_frame, bg="black")
        items_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

        self.label_jouable = tk.Label(self,
                                      image=self.image_jouable,
                                      text=self.personnage_jouable,
                                      compound=tk.TOP)
        self.label_enemi = tk.Label(self,
                                    image=self.image_enemi,
                                    text=self.personnage_ennemi,
                                    compound=tk.TOP)
        self.msg_info = f"Vous rencontrez un {self.personnage_ennemi.nom}"
        self.label_info = tk.Label(self, text=self.msg_info)
        self.bouton_attaquer = tk.Button(self, text="Attaquer", command=self.on_btn_attaquer_click)
        self.bouton_magie = tk.Button(self, text="Magie", command=self.on_btn_magie_click)
        self.bouton_changer_slug = tk.Button(self, text="Changer Slug", command=self.on_btn_choisir_slug_click)
        self.bouton_fuir = tk.Button(self, text="Fuir", command=self.on_btn_fuir_click)


        # --- Actions ---
        action_frame = Frame(self, bg="black")
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)


        self.msg_info = f"Vous rencontrez un {self.personnage_ennemi.nom}"
        self.label_info = tk.Label(self, text=self.msg_info)
        self.bouton_attaquer = RoundedButton(action_frame, "Attaquer", command=self.on_btn_attaquer_click, radius=10, bg="darkgray",
                                         width=100)
        self.bouton_magie = RoundedButton(action_frame, text="Magie", command=self.on_btn_magie_click, radius=10, bg="darkgray",
                                         width=100)
        self.bouton_changer_slug = RoundedButton(action_frame, text="Changer Slug", command=self.on_btn_choisir_slug_click, radius=10, bg="darkgray",
                                         width=100)
        self.bouton_fuir = RoundedButton(action_frame, text="Fuir", command=self.on_btn_fuir_click, radius=10, bg="darkgray",
                                         width=100)
        self.bouton_potion = RoundedButton(action_frame, text="Potion", command=self.utiliser_potion, radius=10, bg="darkgray",
                                           width=100)

        self.bouton_fuir.grid(row=0, column=0, padx=5)
        self.bouton_magie.grid(row=0, column=1, padx=5)
        self.bouton_attaquer.grid(row=0, column=2, padx=5)
        self.bouton_changer_slug.grid(row=0, column=3, padx=5)
        self.bouton_potion.grid(row=5, column=0, padx=5)

        inv_frame.columnconfigure(0, weight=1)
        inv_frame.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.desactiver_controles()

    def placer_widgets(self):
        # Combattants
        self.label_jouable.grid(row=0, column=0)
        self.label_enemi.grid(row=0, column=1)
        # Actions
        self.bouton_attaquer.grid(row=1, column=0, sticky=EW)
        self.bouton_magie.grid(row=2, column=0, sticky=EW)
        self.bouton_fuir.grid(row=1, column=1, sticky=EW)
        self.bouton_changer_slug.grid(row=2, column=1, sticky=EW)
        # Messages
        self.label_info.grid(row=3, column=0, columnspan=2)

    """def on_btn_attaquer_click(self):
        txt1 = self.personnage_jouable.frapper(self.personnage_ennemi)
        if self.personnage_ennemi.est_mort():
            reponse = showinfo("TITRE", "DEAD")
            self.cacher()
        else:
            txt2 = self.personnage_ennemi.frapper(self.personnage_jouable)
            self.msg_info = f"{txt1}\n{txt2}"
            self.actualiser()"""

    def on_btn_attaquer_click(self):
        txt1 = self.personnage_jouable.frapper(self.personnage_ennemi)
        self.actualiser()  # Update after player attack to show damage
        if self.personnage_ennemi.est_mort():
            showinfo("Victoire !", "Vous avez gagné le combat !")
            self.personnage_jouable.gagner_experience(self.personnage_ennemi.experience)
            self.combat_termine = True
            self.cacher()  # Hide combat window

        elif self.personnage_jouable.est_mort():  # Check after each attack
            showinfo("Défaite !", "Votre slug a été vaincu !")
            self.combat_termine = True
            self.cacher()  # Hide combat window after slug faints.

        else:  # Enemy attacks only if neither player or enemy slug has fainted.
            txt2 = self.personnage_ennemi.frapper(self.personnage_jouable)
            self.msg_info = f"{txt1}\n{txt2}"
            self.actualiser()  # Update again to reflect enemy damage

    def on_btn_fuir_click(self):
        showinfo("Fuite", "Vous avez fui le combat !")  # Maybe add a penalty later?
        self.combat_termine = True
        self.cacher()

    def on_btn_choisir_slug_click(self):
        # Implement your slug selection logic here. For now, just a placeholder:
        showinfo("Choisir Slug", "Fonctionnalité à venir !")

        # Example (replace with your actual logic):
        '''new_slug_id = "CHARA_INFURNUS"  # Example new slug
        self.personnage_jouable = Perso(new_slug_id)
        self.charger_images()  # Reload image
        self.actualiser()'''

    def on_btn_magie_click(self):
        showwarning(title="Non implémenté",
                    message="Permettre de choisir un sort.")

    def on_key_press(self, event):
        if event.keysym == "Escape":
            self.destroy()

    def actualiser(self):
        self.label_jouable.config(text=self.personnage_jouable)
        self.label_enemi.config(text=self.personnage_ennemi)
        self.label_info.config(text=self.msg_info)

    def cacher(self):
        self.grab_release()
        self.destroy()

    def desactiver_controles(self):
        self.grab_set()

    def utiliser_potion(self):

        potions = []
        for obj_id, count in self.game.inventaire.tab.items():
            if obj_id.startswith("ITEM_POTION"):
                potions.append((obj_id, count))

        if potions:
            potion_id = potions[0][
                0]
            potion = Objet(potion_id)

            resultat = potion.utiliser(self.personnage_jouable)
            if resultat:
                showinfo("Potion utilisée", resultat)
                self.actualiser()
                self.game.inventaire.enlever(potion)
                # self.game.sauvegarder_partie("sauv01")


        else:  # No potions in inventory to be used.
            showinfo("Pas de potions", "Vous n'avez pas de potions dans votre inventaire.")


if __name__ == "__main__":
    root = tk.Tk()
    personnage_jouable = Perso("CHARA_RAMMSTONE")
    personnage_enemi = Perso("CHARA_PEKUN")

    interface = InterfaceCombat(root, personnage_jouable, personnage_enemi)
    #interface.pack()

    root.bind("<Escape>", interface.on_key_press)

    root.mainloop()
