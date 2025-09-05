import tkinter as tk
from back_magie import *
from tkinter import Listbox, Button, messagebox

# Initialisation d'un tableau vide pour le grimoire du joueur
grimoire_joueur = Grimoire([...])

# TODO : À transformer en classe (utiliser une fenêtre TopLevel)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Ma Fenêtre Tkinter")
#fenetre.geometry("300x300")

label_instruction = tk.Label(fenetre, text="Sélectionnez un sort à invoquer :")
label_instruction.grid()

# Création de la listbox pour afficher les sorts avec une taille plus grande
lst_sorts = Listbox(fenetre, width=50, height=15)  # Largeur et hauteur agrandies
for sort in grimoire_joueur:
    lst_sorts.insert(tk.END, f"{sort['nom_carte']} (Coût: {sort['mana']})")
lst_sorts.grid()


def invoquer(lst, grimoire):
    selection = lst.curselection()
    if len(selection) == 1:
        index = selection[0]
        sort = grimoire[index]

        # Demande de confirmation
        if messagebox.askokcancel("Confirmation", f"Voulez-vous vraiment invoquer {nom(sort)} ?"):
            messagebox.showinfo("Sort lancé", "Vous avez lancé:"+nom(sort))
    elif len(selection) == 0:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un sort.")
    else:
        messagebox.showwarning("Multiple sélections", "Veuillez sélectionner un seul sort.")

btn_invoke = Button(fenetre, text="Invoquer le sort", command=lambda: invoquer(lst_sorts, grimoire_joueur))
btn_invoke.grid()




# Lancer la boucle principale de l'application
fenetre.mainloop()
