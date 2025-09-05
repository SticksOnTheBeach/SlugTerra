from tkinter import *
from back_objet import *
from PIL import Image, ImageTk
from back_game import *
from tkinter import Listbox, Label, Frame, PhotoImage

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

class FenetreAchat(Toplevel):
    def __init__(self, master, a_vendre: Inventaire, inventaire_joueur: Inventaire, jeu :Game):
        super().__init__(master)
        self.title("Achat")
        self.configure(bg="black")
        self.attributes('-alpha', 0.7)

        #  --- Fenetre  ---
        self.transient(master)
        self.lift()
        self.resizable(False, False)
        self.grab_set()

        # Supprimer les boutons de la fenêtre (fermer, réduire, etc.)
        self.overrideredirect(True)

        self.a_vendre = a_vendre
        self.inventaire_joueur = inventaire_joueur


        self.game = jeu
        self.charger_images()
        self.creer_widgets()
        self.placer_widgets()
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
        self.images = {}
        try:
            for obj_id in self.a_vendre:
                obj = Objet(obj_id)
                img_path = obj.icon
                self.images[obj.id] = PhotoImage(file=img_path)
        except Exception as e:
            print(f"Error loading images in shop: {e}")




    # ---------------------------------------

    # --- NOUVELLE FONCTIONS : TOUS LES ITEMS SONT STOCKES DANS DES BOUTONS, QUAND ON CLIQUE SUR LES OBJETS, ON LES ACHETES
    def creer_widgets(self):
        # --- OBJETS MARCHANDS ---
        inv_frame = LabelFrame(self, text="Objets à vendre", bg="black", fg="white")
        inv_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.or_label = Label(inv_frame, text=f"Or: {self.game.inventaire.or_disponible}", bg="black", fg="white")
        self.or_label.grid(row=0, column=0, columnspan=2, sticky="ew")


        items_frame = Frame(inv_frame, bg="black")
        items_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

        self.boutons_objets = []


        # A CHANGER
        for obj_id in self.a_vendre:
            item_frame = Frame(items_frame, bg="black")
            obj = Objet(obj_id)
            image = self.images.get(obj.id)

            bouton_objet = Button(item_frame, text=obj.nom, image=image, compound=LEFT,
                                  command=lambda o=obj: self.demander_confirmation(o),
                                  bg="black", fg="white",
                                  activebackground="darkgray", activeforeground="white",
                                  borderwidth=0, highlightthickness=0)
            bouton_objet.pack(pady=5, padx=5)
            self.boutons_objets.append((bouton_objet, obj))
            item_frame.pack()

        # --- Actions ---
        action_frame = Frame(self, bg="black")
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.btn_acheter = RoundedButton(action_frame, "Acheter", self.acheter_objet, radius=10, bg="darkgray",
                                         width=100)
        self.btn_annuler = RoundedButton(action_frame, "Quitter", self.on_btn_quitter_click, radius=10, bg="darkgray",
                                         width=100)
        #self.btn_acheter.grid(row=0, column=0, padx=5)
        self.btn_annuler.grid(row=0, column=1, padx=5)

        inv_frame.columnconfigure(0, weight=1)
        inv_frame.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def demander_confirmation(self, obj: Objet):
        if messagebox.askyesno("Confirmation d'achat", f"Voulez-vous acheter {obj.nom} pour {obj.prix_achat} or ?"):
            self.acheter_objet(obj)

    def placer_widgets(self):
        self.btn_acheter.grid(row=0, column=0)
        self.btn_annuler.grid(row=0,column=1)


    def acheter_objet(self, obj: Objet):  # nouvelle fonction d'achat

        if self.game.inventaire.depenser_or(obj.prix_achat):
            self.inventaire_joueur.ajouter([obj])
            self.game.sauvegarder_partie("sauv01")
            self.or_label.config(text=f"Or : {self.game.inventaire.or_disponible}")
            messagebox.showinfo("Achat réussi !", f"Vous avez acheté {obj.nom} pour {obj.prix_achat} or .")

        else:
            messagebox.showinfo("Or insuffisant !", "Vous n'avez pas assez d'or pour cet achat.")

    def on_btn_quitter_click(self):
        self.destroy()


if __name__ == "__main__":
    objets_a_vendre = Inventaire()
    objets_a_vendre.ajouter("ITEM_SWORD1")
    objets_a_vendre.ajouter("ITEM_POTION1")
    objets_a_vendre.ajouter("ITEM_KEY")


    app = Tk()
    btn = Button(app,
                text="Faire un achat",
                command=lambda: FenetreAchat(app, objets_a_vendre))
    btn.grid()
    sub = FenetreAchat(app, objets_a_vendre)
    app.mainloop()
