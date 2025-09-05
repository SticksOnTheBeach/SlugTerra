from tkinter import *
from tkinter.ttk import Combobox
from random import choice, randint
import json


# VARIABLES MODIFIABLES DU PROGRAMME
# Taille des images
TILE_SIZE = 64
# Largeur et hauteur initiale de la carte
INITIAL_WIDTH = 16   
INITIAL_HEIGHT = 12
# Dictionnaire liant identifiant et fichier image
# (peut être importé depuis un fichier json)
with open("datas/data_tuiles.json", mode='r', encoding="utf8") as fichier:
    datas = json.load(fichier)
DICO_TILES = {tile_id:datas[tile_id]["image"] for tile_id in datas}

# Nom du fichier carte initial
# None si aucun
# nom d'un fichier si vous souhaitez importer une carte existante
INITIAL_FILE = None 


# A MODIFIER A VOS RISQUES ET PERILS

class MapManager(Tk):
    def __init__(self, dico_tiles: dict, filename: str = None):
        Tk.__init__(self)
        self.title("Gestionnaire de carte")
        self.datas = dico_tiles
        self.tiles_id = list(self.datas.keys())

        self.width = INITIAL_WIDTH
        self.height = INITIAL_HEIGHT
        if filename is None:
            self.carte = self.generer_carte()
        else:
            fichier = open(filename, mode="r", encoding="utf-8")
            self.carte = json.load(fichier)["Carte"]
            fichier.close()
        self.activeLayer = StringVar(self, value="couche1_id")
        self.pencilType = StringVar(self, value="pen")
        self.creer_widgets()
        self.images = self.charger_images()
        self.configurer_widgets()
        self.organiser_widgets()
        self.actualiser()
        self.mainloop()
    
    def generer_carte(self) -> list:
        carte = []
        terrain = self.tiles_id[0]
        for r in range(self.height):
            ligne = []
            for c in range(self.width):
                ligne.append({"couche1_id":terrain,
                              "couche2_id":None})
            carte.append(ligne)
        return carte
    
    def creer_widgets(self):
        self.can = Canvas(self,
                          background="black",
                          width=800, height=600,
                          scrollregion=(0,0,TILE_SIZE*self.width,TILE_SIZE*self.height))
        self.hrule = Scrollbar(self,
                               orient=HORIZONTAL,
                               command=self.can.xview)
        self.vrule = Scrollbar(self,
                               orient=VERTICAL,
                               command=self.can.yview)
        self.deroul = Combobox(self,values=self.tiles_id)
        self.btn_quitter = Button(self,
                                  text="❌ Quitter",
                                  command=self.destroy) #✅
        self.btn_save = Button(self,
                               text="💾 Sauvegarder",
                               command=self.on_btn_save_click)
        self.btn_add_column = Button(self,
                                     text="➕ colonne")
        self.btn_add_row = Button(self,
                                  text="➕ ligne")
        self.btn_del_column = Button(self,
                                     text="➖ colonne")
        self.btn_del_row = Button(self,
                                  text="➖ ligne")
        self.radio_layer1 = Radiobutton(self,
                                        text="Couche 1",
                                        variable=self.activeLayer,
                                        value="couche1_id")
        self.radio_layer2 = Radiobutton(self,
                                        text="Couche 2",
                                        variable=self.activeLayer,
                                        value="couche2_id")
        self.frame_pencil = Frame(self)#, borderwidth=1, relief=SOLID)
        self.radio_pencil1 = Radiobutton(self.frame_pencil,
                                         text="✏️",
                                         variable=self.pencilType,
                                         value="pen")
        self.radio_pencil2 = Radiobutton(self.frame_pencil,
                                        text="🖌️",
                                        variable=self.pencilType,
                                        value="brush")
        self.radio_pencil3 = Radiobutton(self.frame_pencil,
                                        text="🧽️",
                                        variable=self.pencilType,
                                        value="sponge")
        self.lbl_coord = Label(self, text="")
    
    def organiser_widgets(self):
        self.can.grid(row=0, column=0, rowspan=10)
        self.hrule.grid(row=10, column=0, sticky=EW)
        self.vrule.grid(row=0, column=1, rowspan=10, sticky=NS)

        self.btn_add_column.grid(row=0, column=2, sticky=EW)
        self.btn_add_row.grid(row=0, column=3, sticky=EW)
        self.btn_del_column.grid(row=1, column=2, sticky=EW)
        self.btn_del_row.grid(row=1, column=3, sticky=EW)

        self.frame_pencil.grid(row=2, column=2, columnspan=2, sticky=EW)
        self.radio_pencil1.grid(row=0, column=0, sticky=EW)
        self.radio_pencil2.grid(row=0, column=1, sticky=EW)
        self.radio_pencil3.grid(row=0, column=2, sticky=EW)

        self.deroul.grid(row=3, column=2, columnspan=2, sticky=EW)
        self.radio_layer1.grid(row=4, column=2, sticky=EW)
        self.radio_layer2.grid(row=4, column=3, sticky=EW)

        self.btn_quitter.grid(row=8, column=2)
        self.btn_save.grid(row=8, column=3)
        self.lbl_coord.grid(row=9, column=2, columnspan=2, sticky=EW)
    
    
    def configurer_widgets(self):
        self.can.config(xscrollcommand=self.hrule.set,
                        yscrollcommand=self.vrule.set)
        self.can.bind("<Button-1>",self.on_click)
        self.can.bind("<Motion>", self.on_move)
        self.deroul.set(self.tiles_id[0])
        self.btn_add_column.config(foreground="green",
                                   command=self.on_btn_add_col_click)
        self.btn_del_column.config(foreground="red",
                                   command=self.on_btn_del_col_click)
        self.btn_add_row.config(foreground="green",
                                command=self.on_btn_add_row_click)
        self.btn_del_row.config(foreground="red",
                                command=self.on_btn_del_row_click)
    
    def charger_images(self) -> dict:
        dico = {}
        path = "art/tiles/"
        for tile_id in self.tiles_id:
            dico[tile_id] = PhotoImage(file=path+self.datas[tile_id])
        return dico
    
    def actualiser(self):
        self.can.delete("all")
        self.can.config(scrollregion=(0,0,TILE_SIZE*self.width,TILE_SIZE*self.height))
        for r in range(len(self.carte)):
            for c in range(len(self.carte[0])):
                couche1_id = self.carte[r][c]["couche1_id"]
                couche2_id = self.carte[r][c]["couche2_id"]
                self.can.create_image(TILE_SIZE*c,
                                      TILE_SIZE*r,
                                      image=self.images[couche1_id],
                                      anchor=NW)
                if couche2_id is not None:
                    self.can.create_image(TILE_SIZE*c,
                                          TILE_SIZE*r,
                                          image=self.images[couche2_id],
                                          anchor=NW)

    def effacer(self, row, col):
        self.carte[row][col]["couche2_id"] = None

    def remplacer(self, row, col):
        self.carte[row][col][self.activeLayer.get()] = self.deroul.get()

    def colorier(self, row, col, initial_value:str):
        r,c,l = row, col, self.activeLayer.get()
        if 0 <= c < self.width and 0 <= r < self.height and self.carte[r][c][l] == initial_value:
            self.remplacer(row, col)
            self.colorier(r+1, col, initial_value)
            self.colorier(r-1, col, initial_value)
            self.colorier(r, col+1, initial_value)
            self.colorier(r, col-1, initial_value)

    def on_click(self, evt: Event):
        c = int(self.can.canvasx(evt.x) // TILE_SIZE)
        r = int(self.can.canvasy(evt.y) // TILE_SIZE)
        if 0 <= c < self.width and 0 <= r < self.height:
            if self.pencilType.get() == "pen":
                self.remplacer(r,c)
            elif self.pencilType.get() == "sponge":
                self.effacer(r,c)
            elif self.pencilType.get() == "brush":
                v = self.carte[r][c][self.activeLayer.get()]
                self.colorier(r, c, v)
            self.actualiser()
        else:
            print("case invalide")
    
    def on_btn_add_col_click(self):
        for r in range(self.height):
            self.carte[r].append(self.deroul.get())
        self.width += 1
        self.actualiser()
    
    def on_btn_del_col_click(self):
        if self.width > 1:
            for r in range(self.height):
                self.carte[r].pop(-1)
            self.width -= 1
            self.actualiser()
        else:
            print("Suppression de colonne impossible")
    
    def on_btn_add_row_click(self):
        ligne = []
        for c in range(self.width):
            ligne.append(self.deroul.get())
        self.carte.append(ligne)
        self.height += 1
        self.actualiser()
    
    def on_btn_del_row_click(self):
        if self.height > 1:
            self.carte.pop(-1)
            self.height -= 1
            self.actualiser()
        else:
            print("Suppression de ligne impossible")

    def on_move(self, evt: Event):
        col = int(self.can.canvasx(evt.x))//64
        row = int(self.can.canvasy(evt.y))//64
        self.lbl_coord.config(text=f"coordonnées : ({row},{col})")

    def on_btn_save_click(self):
        name = "maps/tmp_map" + str(randint(10**6, 10**7 - 1)) + ".json"
        fichier = open(file=name, mode="w", encoding="utf-8")
        print("fichier", name, "créé")
        dico = {
            "Monstres":[],
            "Coffres":[],
            "Teleports":[],
            "Carte":self.carte
        }
        json.dump(dico, fichier, indent=4)
        fichier.close()
        print("fichier", name, "fermé")

     

if __name__ == "__main__":
    app = MapManager(DICO_TILES, INITIAL_FILE)