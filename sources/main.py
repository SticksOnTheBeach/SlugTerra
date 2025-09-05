import tkinter as tk
from tkinter import Frame, Label, Button, PhotoImage, Toplevel, messagebox
import os
from back_game import Game, charger_partie
from interface_carte import Ecran_Carte


class InterfaceDemarrage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)  # Remplit toute la fenêtre
        # Configurer le fond de la fenêtre principale
        self.configure(bg="red")

        self.splash_img = PhotoImage(file="art/splashscreen.png")
        self.splash_lbl = Label(self, image=self.splash_img)
        self.splash_lbl.pack(side=tk.TOP)
        self.label = Label(self, text="SlugTerra", font=("Helvetica", 16), fg="Black", bg="red")
        self.label.pack(pady=20)

        self.new_game_button = Button(self, text="Nouvelle Partie", fg="Black", command=self.nouvelle_partie)
        self.new_game_button.pack(pady=10)

        self.load_game_button = Button(self, text="Charger Partie", command=self.ouvrir_fenetre_de_chargement)
        self.load_game_button.pack(pady=10)

        self.parameters_button = Button(self, text="Paramètres", command=self.ouvrir_fenetre_de_parametres)
        self.parameters_button.pack(pady=10)

        self.exit_button = Button(self, text="Quitter", command=self.exit)
        self.exit_button.pack(pady=10)

    def ouvrir_fenetre_de_parametres(self):
        self.master.withdraw()
        self.n_window = Toplevel(self.master)
        # self.n_window.geometry("400x400")
        self.n_window.title("Parametres")
        self.n_window.configure(bg="red")

        label1 = Label(self.n_window, text="Parametres", font=("Helvetica", 14), fg="Black", bg="red")
        label1.pack(pady=10)

        # Bouton "Précédent" pour revenir à la fenêtre principale
        back1_button = Button(self.n_window, text="Précédent", command=self.revenir_au_menu_principal1)
        back1_button.pack(pady=10)

    def ouvrir_fenetre_de_chargement(self):
        """Ouvrir une nouvelle fenêtre pour charger une partie et masquer la fenêtre principale."""
        # Masquer la fenêtre principale
        self.master.withdraw()
        # Créer une nouvelle fenêtre (Toplevel)
        self.new_window = Toplevel(self.master)
        self.new_window.title("Charger Partie")
        # self.new_window.geometry("400x300")
        self.new_window.configure(bg="red")

        # Ajouter des éléments dans la nouvelle fenêtre
        label = Label(self.new_window, text="Sélectionnez une partie à charger", font=("Helvetica", 14), bg="red")
        label.pack(pady=20)

        # Bouton Charger la Dernière Sauvegarde
        load_button = Button(self.new_window, text="Charger la Dernière Sauvegarde",
                             command=self.charger_partie_depuis_fenetre)
        load_button.pack(pady=10)

        # Bouton "Précédent" pour revenir à la fenêtre principale
        back_button = Button(self.new_window, text="Précédent", command=self.revenir_au_menu_principal)
        back_button.pack(pady=10)

    def charger_partie_depuis_fenetre(self):
        """Charger une partie depuis la nouvelle fenêtre et lancer la partie."""
        try:
            # Charger la partie sauvegardée
            saved_game = charger_partie("sauv01")  # Tu peux modifier pour demander un fichier spécifique
            self.lancer_partie(saved_game)
            self.new_window.destroy()
            self.revenir_au_menu_principal()

        except FileNotFoundError:
            # Gérer l'erreur si le fichier de sauvegarde n'existe pas
            error_label = Label(self.new_window,
                                text="Erreur : fichier de sauvegarde introuvable", fg="red",
                                bg="lightblue")
            error_label.pack(pady=10)

    def revenir_au_menu_principal(self):
        """Fermer la fenêtre de chargement et réafficher la fenêtre principale."""
        self.new_window.destroy()
        self.master.deiconify()  # Réafficher la fenêtre principale

    def revenir_au_menu_principal1(self):
        """Fermer la fenêtre de chargement et réafficher la fenêtre principale."""
        self.n_window.destroy()
        self.master.deiconify()  # Réafficher la fenêtre principale

    def nouvelle_partie(self):
        """Lancer une nouvelle partie avec le fichier par défaut ou demander confirmation si une sauvegarde existe."""
        # Chemin du fichier de sauvegarde
        save_file_path = "saves/sauv01.json"  # Remplacez par le nom_carte du fichier de sauvegarde si nécessaire
        # Vérifier si une sauvegarde existe déjà
        if os.path.exists(save_file_path):
            # Demander confirmation à l'utilisateur
            confirmation = messagebox.askyesno("Confirmation",
                                               "Voulez-vous vraiment lancer une nouvelle partie ? Cette action écrasera la sauvegarde actuelle.")
            if not confirmation:
                return  # L'utilisateur a annulé, ne pas lancer la nouvelle partie
        # Si aucune sauvegarde n'existe ou si l'utilisateur confirme, lancer la nouvelle partie
        default_game = charger_partie("default")
        self.lancer_partie(default_game)

    def lancer_partie(self, game):
        # Lancer linterface de jeu avec la carte donnée.
        self.pack_forget()  # Supprime le menu de démarrage
        ecran_carte = Ecran_Carte(self.master, game)
        ecran_carte.grid()

    def exit(self):
        self.master.destroy()


# Inutilisable en dehors d'OS windows ou Linux → nécéssite une approche différente via les fonctionnalités de base
# de TKinter pour MacOS

"""def arrondir_bords_fenetre(fenetre, radius):
    hwnd = windll.user32.GetParent(fenetre.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(hwnd, 2, byref(c_int(1)), sizeof(c_int))

    windll.user32.SetWindowRgn(hwnd,
                                windll.gdi32.CreateRoundRectRgn(0, 0, fenetre.winfo_width(), fenetre.winfo_height(),
                                                                radius, radius), True)"""

if __name__ == "__main__":
    # Initialisation de la fenêtre principale Tkinter
    root = tk.Tk()
    # root.geometry("440x380")  # Taille de la fenêtre

    # Application de coins arrondis à la fenêtre principale (seulement pour Windows)
    root.update_idletasks()  # Assure-toi que la fenêtre est rendue avant de modifier ses propriétés
    # arrondir_bords_fenetre(root, 30)  # Applique des coins arrondis avec un rayon de 30 pixels

    # Création de l'interface de démarrage
    app = InterfaceDemarrage(root)

    # Démarrage de la boucle principale Tkinter
    root.mainloop()
