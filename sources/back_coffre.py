import tkinter as tk
from tkinter import messagebox
from back_objet import Objet  # Assurez-vous que ce module existe et est accessible
import json

def afficher_contenu(coffre):
    """
    Affiche le contenu d'un coffre via une boîte de dialogue.

    Cette fonction prend un objet `Coffre` en entrée et affiche son contenu
    dans une boîte de message. Si le coffre est vide ou n'existe pas, un
    message approprié est affiché. Si le coffre est fermé, il est ouvert avant
    d'afficher le contenu.

    :param coffre: Instance de la classe `Coffre` représentant le coffre à afficher.
                    Si `coffre` est `None`, un message indiquant que le coffre est vide
                    ou inexistant est affiché.
    :type coffre: Coffre ou None

    :raises AttributeError: Si `coffre` n'est pas une instance de la classe `Coffre`
                           et ne possède pas les attributs `est_ouvert` et `contenu`.

    :note: La fonction utilise la méthode `ouvrir()` de l'objet `Coffre` pour
           ouvrir le coffre s'il est initialement fermé.

    :example:
    >>> coffre = Coffre(["épée", "bouclier"])
    >>> afficher_contenu(coffre)  # Affiche une boîte de message avec le contenu du coffre
    """
    if coffre is None:
        messagebox.showinfo("Coffre", "Ce coffre est vide ou inexistant.")
    elif coffre.est_ouvert:
        if coffre.contenu:
            messagebox.showinfo("Coffre", f"Vous trouvez dans le coffre : {', '.join(obj.nom for obj in coffre.contenu)}")
        else:
            messagebox.showinfo("Coffre", "Le coffre est déjà ouvert et vide.")
    else:
        coffre.ouvrir()
        if coffre.contenu:
            messagebox.showinfo("Coffre", f"Vous ouvrez le coffre et trouvez : {', '.join(obj.nom for obj in coffre.contenu)}")
        else:
            messagebox.showinfo("Coffre", "Le coffre est vide.")


class Coffre:
    """
    Représente un coffre qui peut contenir des objets.

    Un coffre a un contenu (une liste d'objets) et un état (ouvert ou fermé).
    """
    def __init__(self, contenu:list = []):
        """
        Initialise un nouveau coffre.

        :param contenu: Liste des identifiants (IDs) des objets initialement présents dans le coffre.
                       Par défaut, le coffre est initialisé vide.
        :type contenu: list
        """

        self.contenu = []
        for obj_id in contenu:
            self.contenu.append(Objet(obj_id))  # Crée des instances d'Objet à partir des IDs
        self.est_ouvert = False  # Le coffre est initialement fermé


    def ouvrir(self):
        """
        Ouvre le coffre.

        Si le coffre est déjà ouvert, cette méthode ne fait rien.
        Si le coffre est fermé, son état passe à ouvert.

        :return: Le contenu du coffre si celui-ci est ouvert avec succès, sinon une liste vide.
        :rtype: list
        """
        if not self.est_ouvert:
            self.est_ouvert = True
            return self.contenu #if self.contenu else "Vide"
        else:
            return []#"Coffre déjà ouvert."

    def fermer(self):
        """
        Ferme le coffre.

        Si le coffre est déjà fermé, une exception est levée.
        """
        if self.est_ouvert:
            self.est_ouvert = False
        else:
            raise IndexError("le coffre est dejà fermé.")


    def vider(self) -> list:
        """
        Vide le contenu du coffre s'il est ouvert.

        :return: Une liste vide si le coffre est ouvert. Sinon, retourne le contenu actuel du coffre.
        :rtype: list
        """
        if self.est_ouvert:
            contenu = self.contenu
            self.contenu = []
            return contenu
        if not self.est_ouvert:
            return self.contenu


class FenetreCoffre(tk.Toplevel):
    """
    Représente une fenêtre affichant le contenu d'un coffre.

    Cette classe hérite de `tk.Toplevel` et affiche une fenêtre qui
    présente le contenu textuel d'un coffre.
    """
    def __init__(self, parent, contenu_coffre):
        """
        Initialise la fenêtre du coffre.

        :param parent: Le widget parent de cette fenêtre. Généralement la fenêtre principale de l'application.
        :type parent: tk.Widget

        :param contenu_coffre: Une liste de chaînes de caractères représentant le contenu du coffre.
                                Chaque élément de la liste sera affiché dans la fenêtre.
        :type contenu_coffre: list
        """
        super().__init__(parent)
        self.title("Coffre ouvert !")
        self.geometry("400x300")

        # Création du Canvas
        canvas = tk.Canvas(self, width=400, height=300)
        canvas.pack()

        # Affichage du message dans le Canvas
        canvas.create_text(200, 30, text="Bravo ! Voici ce que contenait le coffre :", font=('Arial', 12))

        # Affichage du contenu du coffre
        y_offset = 70  # Position de départ pour le contenu
        for item in contenu_coffre:
            canvas.create_text(200, y_offset, text=item, font=('Arial', 10))
            y_offset += 30  # Décaler vers le bas

        # Ajouter une image si nécessaire
        # Si vous avez une image à ajouter, décommentez la ligne suivante et remplacez le chemin par celui de votre image
        # image = tk.PhotoImage(file="path_to_image.png")
        # canvas.create_image(200, y_offset + 20, image=image)

        # Fermer la fenêtre après un clic
        close_button = tk.Button(self, text="Fermer", command=self.destroy)
        close_button.pack(pady=10)



# Canva pour l'affichage des coffres
class Application(tk.Tk):
    """
    Représente l'application principale avec une interface graphique simple.

    Cette application contient un bouton pour ouvrir un coffre et affiche le contenu
    du coffre dans une fenêtre séparée.
    """
    def __init__(self):
        """
        Initialise l'application.
        """
        super().__init__()
        self.title("Coffre")
        self.geometry("300x200")

        # Créer un coffre
        self.coffre = Coffre(["épée", "potion"])  # Initialise le coffre avec un contenu

        # Bouton pour ouvrir le coffre
        open_button = tk.Button(self, text="Ouvrir le coffre", command=self.ouvrir_coffre)
        open_button.pack(pady=50)

    def ouvrir_coffre(self):
        """
        Ouvre le coffre et affiche son contenu dans une nouvelle fenêtre.
        """
        contenu_coffre = self.coffre.ouvrir()
        # Ouvrir la fenêtre avec le contenu du coffre
        if contenu_coffre:
            contenu_noms = [obj.nom for obj in contenu_coffre]
            FenetreCoffre(self, contenu_noms)
        else:
            FenetreCoffre(self, ["Le coffre est vide."])


# Lancer l'application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
