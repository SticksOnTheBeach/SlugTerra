
from back_game import *
from back_perso import *
from back_objet import *
from tkinter import *
import tkinter as tk
from tkinter.messagebox import showinfo
# from PIL import Image, ImageTk


class RoundedButton(Canvas):
    def __init__(self, master, text, command, radius=20, width=100, height=40, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)  #
        self.command = command
        self.radius = radius

        self.bg_color = kwargs.get("bg", "grey") # Default background color
        self.create_rounded_rectangle(2, 2, width - 2, height - 2, fill=self.bg_color, outline="", tags="button")
        self.create_text(width / 2, height / 2, text=text, tags="text", fill="white")

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def create_rounded_rectangle(self, x1, y1, x2, y2, **kwargs):
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

class Ecran_Stats(Toplevel):

    def __init__(self, master, jeu: Game):
        super().__init__(master)
        self.title("Statistiques")
        self.configure(bg="black")
        self.attributes('-alpha', 0.7)

        self.selected_item = None

        #  --- Fenetre  ---
        self.transient(master)
        self.lift()
        self.resizable(False, False)
        #self.grab_set()

        # Supprimer les boutons de la fenêtre (fermer, réduire, etc.)
        self.overrideredirect(True)

        self.game = jeu
        self.charger_images()
        self.charger_images()
        self.create_widgets()
        self.center_window() # Centrer

         # Empêche toutes interractions avec les autres fenetres



    def center_window(self):
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


    """def charger_images(self):
        self.images = {}
        try:
            for perso in self.game.equipe:
                img_path = perso.icon
                self.images[perso.id] = PhotoImage(file=img_path)

            for obj in self.game.inventaire:
                img_path = obj.icon
                self.images[obj.id] = PhotoImage(file=img_path)


        except Exception as e:
            print(f"Error loading images: {e}")"""


    # A CHANGER
    def charger_images(self):
        self.images = {}
        try:
            for perso in self.game.equipe:
                img_path = perso.icon
                self.images[perso.id] = PhotoImage(file=img_path)

            for obj_id, count in self.game.inventaire.tab.items():
                obj = Objet(obj_id)
                img_path = obj.icon
                self.images[obj.id] = PhotoImage(file=img_path)

        except Exception as e:
            print(f"Erreur lors du chargement des images: {e}")



    def create_widgets(self):
        # --- Stats Perso ---
        char_frame = LabelFrame(self, text="Équipe", bg="black", fg="white")
        char_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        for i, perso in enumerate(self.game.equipe):
            Label(char_frame, image=self.images.get(perso.id), bg="black").grid(row=i, column=0)
            Label(char_frame,
                  text=f"{perso.nom}\nPV: {perso.pv}/{perso.pvMax}\nPM: {perso.pm}/{perso.pmMax}\nForce: {perso.force}\nMagie: {perso.magie}\nExp: {perso.experience}",
                  bg="black", fg="white").grid(row=i, column=1, sticky="w")

        # --- Inventaire ---
        inv_frame = LabelFrame(self, text="Inventaire", bg="black", fg="white")
        inv_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")


        Label(inv_frame, text=f"Or: {self.game.inventaire.or_disponible}", bg="black", fg="white").grid(row=0, column=0,
                                                                                                        columnspan=2)

        """for i, obj in enumerate(self.game.inventaire):
            Label(inv_frame, image=self.images.get(obj.id), bg="black").grid(row=i + 1, column=0)
            Label(inv_frame, text=f"{obj.nom}", bg="black", fg="white").grid(row=i + 1, column=1,
                                                                             sticky="w")"""

        """self.lst_obj = Listbox(inv_frame, width=10, height=15, borderwidth=0,
                               highlightthickness=0)
        self.lst_obj.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="nsew")"""

        i = 0
        for obj_id, count in self.game.inventaire.tab.items():

            obj = Objet(obj_id)
            #item_frame = Frame(self.lst_obj, bg="black")
            image = self.images.get(obj.id)
            if image:
                Label(inv_frame, image=image, bg="black").grid(row=i + 1, column=0)
            Label(inv_frame, text=f"{obj.nom} (x{count})", bg="black", fg="white").grid(row=i + 1, column=1, sticky="w")
            i += 1

            """item_frame.bind("<Button-1>",
                            lambda event, o=obj: self.selectionner_objet(o))  # Use lambda to pass the object

            self.lst_obj.insert(END, "")  # Insert a blank line. Correct and Crucial!
            self.lst_obj.itemconfig(END, {"widget": item_frame})  # Configure *that line* with your frame widget.

            i += 1"""


            # --- Actions ---
        action_frame = Frame(self, bg="black")
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)

        RoundedButton(action_frame, "Utiliser", self.utiliser_objet, radius=10, bg="darkgray", width=100).pack(
                side=LEFT, padx=5)
        RoundedButton(action_frame, "Combattant", self.choisir_combattant, radius=10, bg="darkgray",
                          width=100).pack(
                side=LEFT, padx=5)
        RoundedButton(action_frame, "Sauvegarder", lambda: self.game.sauvegarder_partie("sauv01"), radius=10,
                          bg="darkgray", width=100).pack(side=LEFT, padx=5)
        RoundedButton(action_frame, "Quitter", self.destroy, radius=10, bg="darkgray", width=100).pack(side=LEFT,
                                                                                                           padx=5)

    def utiliser_objet(self):
        try:
            selection = self.lst_obj.curselection()[0]  # Get selected item index
            resultat = self.game.inventaire.utiliser_objet(selection, self.game.equipe[0]) # Use item on first slug in the team.  You might change this later to select which slug.
            if resultat:
                showinfo("Résultat", resultat) #Informative feedback.
                self.actualiser_stats() #Update stats display after using item.

        except IndexError:
             showinfo("Aucun objet sélectionné", "Veuillez sélectionner un objet à utiliser.")

    def selectionner_objet(self, obj): #New method to select an item
        self.selected_item = obj #Store selection.
        messagebox.showinfo("Objet selectionné", f"Vous avez selectionné : {obj.nom}")

    def utiliser_objet_selectionne(self): #New method - uses selected object
        if self.selected_item:
            try:

                resultat = self.game.inventaire.utiliser_objet(self.selected_item.id, self.game.equipe[0]) #Find object by ID and use it.

                if resultat:
                    showinfo("Résultat", resultat) #Message to the player
                    self.actualiser_stats()  # Update display
                    self.selected_item = None  #Reset selected item after it's used.
                # ... (handle errors like before if the object can't be used or not found).
            except IndexError:
                pass #TODO: handle error
        else:
            showinfo("Aucun objet selectionné !", "Veuillez selectionner un objet à utiliser.")

    def actualiser_stats(self):

        # --- Character Stats update ---
        for i, perso in enumerate(self.game.equipe):  # Assuming same structure as create_widgets
            # Find the label containing perso's stats and update its text
            for widget in self.winfo_children(): #Iterate over all children of the Ecran_Stats window.
                if isinstance(widget, LabelFrame) and widget.cget("text") == "Équipe": #Find character LabelFrame
                    char_frame = widget
                    break #Exit loop once found.

            # Update stats labels within char_frame (assuming grid layout)
            for j, label in enumerate(char_frame.winfo_children()):
                if isinstance(label, Label) and j == i*2 + 1:  # Assuming image in column 0 and text in column 1 for each row, if there are other widgets in that frame they might cause index or type mismatches.
                   label.config(text=f"{perso.nom}\nPV: {perso.pv}/{perso.pvMax}\nPM: {perso.pm}/{perso.pmMax}\nForce: {perso.force}\nMagie: {perso.magie}\nExp: {perso.experience}")
                   break


        # --- Inventaire Update ---
        # Clear the listbox and repopulate (easier than updating individual items)

        self.lst_obj.delete(0, END) #Clear it
        i = 0
        for obj_id, count in self.game.inventaire.tab.items():  #Refresh inventory after changes.  If no changes to inventory are made, you could also simply update the changed character's stats, but when an item is used up (count becomes zero) it's easiest and cleanest to redraw all items rather than removing the correct row from the Listbox.
            obj = Objet(obj_id)
            item_frame = Frame(self.lst_obj, bg="black")

            image = self.images.get(obj.id)
            if image:
                label_image = Label(item_frame, image=image, bg="black")
                label_image.pack(side=LEFT, padx=(5, 0))

            label_text = Label(item_frame, text=f"{obj.nom} (x{count})", bg="black", fg="white")
            label_text.pack(side=LEFT)


            item_frame.bind("<Button-1>", lambda event, o=obj: self.selectionner_objet(o))
            self.lst_obj.insert(END, "")
            self.lst_obj.itemconfig(END, {"widget": item_frame})
            i += 1

        # Update gold display
        inv_frame.winfo_children()[0].config(text=f"Or: {self.game.inventaire.or_disponible}")

    def choisir_combattant(self):
        print("Choisir Combattant")
        pass  # TODO: Ajouté les combattants (les slugs) à jouer