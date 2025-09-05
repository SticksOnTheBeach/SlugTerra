# | --- Interfaces --- | #
from interface_achat import FenetreAchat
from interface_stats import Ecran_Stats
from interface_combat import *

# | --- Backend --- | #
from back_game import *
from back_objet import Inventaire
from back_marchands import *

# | --- Modules --- | #
from tkinter import *
import tkinter as tk
import json
#from tkinter import Toplevel, Label, Button







class Ecran_Carte(Frame):

    def __init__(self, master, jeu: Game):
        super().__init__(master)

        """self.caneva_carte = Canvas(self,
                                   width=15 * 64, height=11 * 64,
                                   background="black")"""
        self.caneva_carte = Canvas(self,
                                   width=15 * 64, height=11 * 64,
                                   background="black")
        self.game = jeu
        self.charger_images()


        self.label_pas = Label(self, text=f"Pas: {self.game.nb_pas}", font=("Arial", 12), fg="white", bg="black")
        self.label_pas.grid(row=0, column=0)


        self.label_or = Label(self, text=f"Or: {self.game.inventaire.or_disponible}", font=("Arial", 12), fg="yellow",
                              bg="black")
        self.label_or.grid(row=0, column=1)

        self.dialogue_window = None




        # -------------------
        self.creer_interface_joueur()
        self.caneva_carte.grid(row=1, column=0, columnspan=2)
        # -------------------

        self.caneva_carte.grid(row=1, column=0, columnspan=2)


        self.actualiser()
        master.bind("<Key>", self.on_key_press)

    def creer_interface_joueur(self):
        """ *
        Todo : réaliser un innterface qui sera placé juste au-dessus de l'écran de jeu et celui-ci
         devra afficher un rectangle NOIR TRANSPARENT (opacité : 0.7)
          avec 4 carrés qui eux devront contenir les images des slugs/l'équipe
         que le joueur possède. """









    def charger_images(self) -> dict:
        self.img = {}
        try:
            with open(file="datas/data_tuiles.json", mode="r") as fichier:
                donnees_images = json.load(fichier)
                for tile_id in donnees_images:
                    self.img[tile_id] = PhotoImage(file="./art/tiles/" + donnees_images[tile_id]["image"])

            # Chargement des images spécifiques
            try:
                self.img["croix"] = PhotoImage(file="./art/icons/cross.png")
                self.img["coffre_ferme"] = PhotoImage(file="./art/icons/coffre_ferme.png")
                self.img["coffre_ouvert"] = PhotoImage(file="./art/icons/coffre_ouvert.png")
                self.img["hero_haut"] = PhotoImage(file="./art/sprites/hero_up.png")
                self.img["hero_droite"] = PhotoImage(file="./art/sprites/hero_right.png")
                self.img["hero_bas"] = PhotoImage(file="./art/sprites/hero_down.png")
                self.img["hero_gauche"] = PhotoImage(file="./art/sprites/hero_left.png")
                self.img["teleport"] = PhotoImage(file="./art/icons/T_teleport.png")
                self.img["marchand"] = PhotoImage(file="./art/sprites/Marchand.png")
            except Exception as e:
                self.img["marchand"] = None
                print(f"Erreur de chargement des images spécifiques: {e}")



            try:
                self.img["or"] = PhotoImage(file="./art/icons/ITEM_PIECE_OR.png")
            except Exception as e:
                print(f"Erreur de chargement de l'image 'or': {e}")
                # Replace with a placeholder or do not assign if file is missing

            return self.img
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'ouverture du fichier de tuiles: {e}")
            return {}

    def dessiner_carte(self):
        """Dessine les deux couches superposées de la carte."""
        grille = self.game.alentours()
        for i, ligne in enumerate(grille):
            for j, tuile in enumerate(ligne):
                self.dessiner_tuile(i, j, grille)

    def dessiner_tuile(self, l: int, c: int, grille: list) -> None:
        # x, y = c * 64, l * 64
        x, y = c * 64, l * 64
        # TODO : changer la taille des différentes tuiles afin de passer de 64px à 32px
        tuile = grille[l][c]
        if tuile is not None:
            # Dessin de la première couche
            if tuile.couche1_id in self.img:
                self.caneva_carte.create_image(x, y, image=self.img[tuile.couche1_id], anchor=tk.NW, tags="TUILE")
            else:
                print("Aucune image trouvée pour", tuile.couche1_id)
            # Dessin de la deuxième couche (si présente)
            if tuile.couche2_id in self.img:
                self.caneva_carte.create_image(x, y, image=self.img[tuile.couche2_id], anchor=tk.NW, tags="COUCHE2")
            if tuile.contient_coffre():
                if tuile.coffre.est_ouvert:
                    self.caneva_carte.create_image(x, y, image=self.img["coffre_ouvert"], anchor=tk.NW, tags="COFFRE")
                else:
                    self.caneva_carte.create_image(x, y, image=self.img["coffre_ferme"], anchor=tk.NW, tags="COFFRE")
            if tuile.contient_teleport():
                self.caneva_carte.create_image(x, y, image=self.img["teleport"], anchor=tk.NW, tags="TELEPORT")
            if tuile.contient_marchand():
                if self.img.get("marchand"):  # Check if the image was loaded
                    self.caneva_carte.create_image(x, y, image=self.img["marchand"], anchor=tk.NW, tags="MARCHAND")
                else:
                    print("Image du marchand manquante.  Affichage d'un espace réservé ou rien.")
                    self.caneva_carte.create_rectangle(x, y, x + 64, y + 64, fill="red", tags="MARCHAND")

    def effacer_tout(self) -> None:
        self.caneva_carte.delete("all")
        self.caneva_carte.delete("MONTANT_OR")

    def actualiser(self):
        self.effacer_tout()
        self.dessiner_carte()
        self.dessiner_heros()
        self.afficher_or()  # Ajouter ici l'affichage de l'or
        self.label_pas.config(text=f"Pas: {self.game.nb_pas}")

    def dessiner_heros(self):
        """Dessine le héros à sa position et selon sa direction."""
        x_pos = 480
        y_pos = 352
        # Choisir l'image du héros selon sa direction
        if self.game.direction == 0:  # Haut
            self.caneva_carte.create_image(x_pos, y_pos, image=self.img["hero_haut"], tags="HERO")
        elif self.game.direction == 1:  # Droite
            self.caneva_carte.create_image(x_pos, y_pos, image=self.img["hero_droite"], tags="HERO")
        elif self.game.direction == 2:  # Bas
            self.caneva_carte.create_image(x_pos, y_pos, image=self.img["hero_bas"], tags="HERO")
        elif self.game.direction == 3:  # Gauche
            self.caneva_carte.create_image(x_pos, y_pos, image=self.img["hero_gauche"], tags="HERO")

    def on_key_press(self, evt: Event) -> None:

        """if evt.keysym == "H" or evt.keysym == "h":  # Touche pour ouvrir l'interface d'achat
            marchand = self.game.interagir_marchand()
            if marchand:
                self.ouvrir_interface_achat(marchand.inventaire)
            else:
                print("Aucun marchand à proximité.")"""

        if evt.keysym == "H" or evt.keysym == "h":
            marchand = self.game.interagir_marchand()
            if marchand:
                self.afficher_dialogue_marchand(marchand)
                # TODO : self.ouvrir_interface_achat(marchand.inventaire) mettre le dialogue / le message du marchand dans cette ligne de code
            else:
                print("Aucun marchand à proximité.")

        elif evt.keysym == "I" or evt.keysym == "i":
            Ecran_Stats(self, self.game)

        elif evt.keysym == "Escape":
            self.game.sauvegarder_partie("sauv01")
            self.master.destroy()
        elif evt.keysym == "Left" or evt.keysym == "q" or evt.keysym == "Q" :
            self.game.deplacer_gauche()
            self.actualiser()
        elif evt.keysym == "Right" or evt.keysym == "d" or evt.keysym == "D":
            self.game.deplacer_droite()
            self.actualiser()
        elif evt.keysym == "Up" or evt.keysym == "z" or evt.keysym == "Z":
            self.game.deplacer_haut()
            self.actualiser()
        elif evt.keysym == "Down" or evt.keysym == "s" or evt.keysym == "S":
            self.game.deplacer_bas()
            self.actualiser()
        elif evt.keysym == "e" or evt.keysym == "E" or evt.keysym == "Return":  # Touche pour ouvrir un coffre
            self.ouvrir_coffre()
            self.actualiser()
        else:
            print(evt.keysym)

        if self.game.verifier_combat():
            self.ouvrir_interface_combat()

    def ouvrir_interface_combat(self):
        ennemi, exp = self.game.choisir_monstre()
        # TODO : modifier votre personnage en fonction de l'équipe
        ennemi, exp = self.game.choisir_monstre()
        # Récupérer un personnage de l'équipe pour le combat
        ami = self.game.equipe.get(0)  # Utilisez le premier personnage de l'équipe
        assert ami, "Aucun personnage dans l'équipe !"
        InterfaceCombat(self, ami, ennemi, self.game)


    def ouvrir_coffre(self):
        if self.game.peut_ouvrir_un_coffre():
            contenu = self.game.ouvrir_coffre()
            self.afficher_message(contenu)


    def afficher_message(self, mesg:str):
        """Fenêtre pour afficher le contenu du coffre avec un fond noir et opacité semi-transparente, rattachée à la fenêtre principale."""

        # Créer la fenêtre pop-up
        pop_up = Toplevel(self.master)
        pop_up.title("Contenu du Coffre")
        largeur_pop_up, hauteur_pop_up = 300, 200

        # Rendre la fenêtre noire avec opacité semi-transparente
        pop_up.configure(bg='black')  # Fond noir
        pop_up.attributes('-alpha', 0.7)  # Opacité de 70% (valeur entre 0.0 et 1.0)

        # Supprimer les boutons de la fenêtre (fermer, réduire, etc.)
        pop_up.overrideredirect(True)

        # Rendre la fenêtre pop-up rattachée à la fenêtre principale (jeu)
        pop_up.transient(self.master)  # La fenêtre pop-up est attachée à la fenêtre principale
        pop_up.lift()  # La fenêtre pop-up reste au-dessus de la fenêtre principale

        # Obtenir les dimensions de la fenêtre principale pour centrer
        self.master.update_idletasks()
        position_x_master = self.master.winfo_x()
        position_y_master = self.master.winfo_y()
        largeur_master = self.master.winfo_width()
        hauteur_master = self.master.winfo_height()

        position_x_pop_up = position_x_master + (largeur_master - largeur_pop_up) // 2
        position_y_pop_up = position_y_master + (hauteur_master - hauteur_pop_up) // 2

        pop_up.geometry(f"{largeur_pop_up}x{hauteur_pop_up}+{position_x_pop_up}+{position_y_pop_up}")

        # Ajouter un canvas pour afficher le texte
        canvas = Canvas(pop_up, width=largeur_pop_up, height=hauteur_pop_up, bg='black', bd=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Ajouter le contenu
        canvas.create_text(150, 70, text=mesg, font=("Arial", 14), fill="Orange")

        # Ajouter un bouton pour fermer
        bouton_fermer = Button(pop_up, text="Fermer", command=pop_up.destroy)
        canvas.create_window(150, 150, window=bouton_fermer)

    def afficher_or(self):
        """Affiche le montant d'or sur le Canvas avec une icône."""
        # Afficher l'icône d'or
        if "or" in self.img:
            self.caneva_carte.create_image(50, 50, image=self.img["or"], anchor=tk.CENTER, tags="MONTANT_OR")
        else:
            print("Image pour 'or' non trouvée, affichage ignoré.")

        # Afficher le texte à côté
        self.caneva_carte.create_text(
            100, 50,  # Ajustez les coordonnées (X, Y) pour que le texte apparaisse correctement
            text=f"Or : {self.game.inventaire.or_disponible}",  # Montant d'or
            font=("Arial", 16),
            fill="yellow",
            tags="MONTANT_OR")

    def afficher_dialogue_marchand(self, marchand):
        """Affiche la fenêtre de dialogue du marchand, gère la saisie du nom du joueur et l'affichage progressif du texte."""


        """self.fenetre_de_dialogue = Toplevel(self)
        self.fenetre_de_dialogue.transient(self)
        self.fenetre_de_dialogue.overrideredirect(True)
        self.fenetre_de_dialogue.attributes("-alpha", 0.7)"""

        """self.fenetre_de_dialogue = Toplevel(self)
        if self.fenetre_de_dialogue is not None and self.fenetre_de_dialogue.winfo_exists():  # Check for existing dialog window.
            self.fermer_dialogue_marchand()
            self.fenetre_de_dialogue = None"""

        """self.fenetre_de_dialogue = Toplevel(self)
        self.fenetre_de_dialogue.transient(self)"""


        self.dialogue_frame = Frame(self, bg="black", relief="raised", borderwidth=2)
        self.dialogue_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.dialogue_text = "Comment vous appelez-vous ?"  # Store the full text
        self.dialogue_label = Label(self.dialogue_frame, text="",  # Start with empty text
                                    wraplength=self.caneva_carte.winfo_width(), bg="black", fg="white", justify=LEFT)
        self.dialogue_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=10)

        self.afficher_texte_progressif(0, marchand)
        self.desactiver_controles()

        # --- Nom du Joueur ---

        self.nom_joueur = ""
        self.nom = Entry(self.dialogue_frame, bg="white", fg="black")
        self.nom.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.nom.bind("<Return>", lambda event: self.demarrer_dialogue(marchand))

        self.btn_acheter = Button(self.dialogue_frame, text="Acheter", state=DISABLED,
                                  command=lambda: self.ouvrir_interface_achat(marchand.inventaire))
        self.btn_quitter = Button(self.dialogue_frame, text="Quitter", command=self.fermer_dialogue_marchand,
                                  state=DISABLED)

        self.btn_parler = Button(self.dialogue_frame, text="Parler",
                                 command=lambda: self.afficher_dialogue_marchand(marchand),
                                 state=DISABLED)

        self.btn_acheter.grid(row=2, column=0, padx=5, pady=5)
        self.btn_quitter.grid(row=2, column=1, padx=5, pady=5)
        self.btn_parler.grid(row=2, column=2, padx=5, pady=5)

        self.desactiver_controles()


    def afficher_texte_progressif(self, index, marchand):
        if index < len(self.dialogue_text):
            self.dialogue_label.config(text=self.dialogue_text[:index + 1])
            self.after(50, self.afficher_texte_progressif, index + 1, marchand)
        else:
            self.activer_boutons_dialogue()

    def activer_boutons_dialogue(self):
        self.btn_acheter.config(state=NORMAL)
        self.btn_quitter.config(state=NORMAL)
        self.btn_parler.config(state=NORMAL)


    def demarrer_dialogue(self, marchand):
        self.nom_joueur = self.nom.get()
        self.nom.grid_remove()

        self.dialogue_text = f"Enchanté {self.nom_joueur}, je m'appelle Kreto, je suis marchand. Regardez si j'ai quelque chose qui peut vous intéresser."
        self.dialogue_label.config(text="")
        self.afficher_texte_progressif(0, marchand)

    def ouvrir_interface_achat(self, inventaire_marchand):
        self.activer_controles()
        self.fermer_dialogue_marchand()
        FenetreAchat(self, inventaire_marchand, self.game.inventaire, self.game)

    def fermer_dialogue_marchand(self):
        """Ferme la fenêtre de dialogue du marchand, réactive les contrôles et rend les fonctionnalités/la main à la fenêtre principale.
        """
        print("fermeture de la fenetre en cours...")
        self.dialogue_frame.grid_forget()

        self.activer_controles()
        self.focus_set()

    def desactiver_controles(self):
        self.grab_set()


    def activer_controles(self):
        self.bind("<Key>", self.on_key_press)

    def ouvrir_interface_achat(self, inventaire_marchand):
        FenetreAchat(self, inventaire_marchand, self.game.inventaire, self.game)



if __name__ == "__main__":
    jeu = charger_partie("default")
    app = Tk()
    cnv = Ecran_Carte(app, jeu)
    cnv.grid()
    app.mainloop()
