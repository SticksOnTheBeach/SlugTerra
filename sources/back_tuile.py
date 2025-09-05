from back_coffre import Coffre
from back_marchands import Marchand
import json


def charger_toutes_les_tuiles():
    with open('datas/data_tuiles.json', 'r') as fichier:
        return json.load(fichier)

class Tuile:
    def __init__(self, couche1_id: str, couche2_id: str = None, coffre=None):
        datas = charger_toutes_les_tuiles()
        self.couche1_id = couche1_id
        self.couche2_id = couche2_id
        self.terrain = datas[self.couche1_id]["nom"]
        self.coffre = coffre
        self.teleport = None
        self.marchand = None
        if couche2_id is None:
            self.traversable = datas[self.couche1_id]["traversable"]
        else:
            self.traversable = datas[self.couche1_id]["traversable"] and datas[couche2_id]["traversable"]

    def contient_coffre(self) -> bool:
        """
        Vérifie si la tuile contient un coffre.

        :return: True si la tuile contient un coffre, False sinon.
        """
        return self.coffre is not None

    def ouvrir_coffre(self) -> list:
        """
        Ouvre le coffre s'il y en a un.

        :return: Contenu du coffre si présent et non vide, None sinon.
        """
        if self.contient_coffre():
            if not self.coffre.est_ouvert:
                self.coffre.ouvrir()
                return self.coffre.contenu
        return []

    def ajouter_coffre(self, contenu:list):
        self.coffre = Coffre(contenu)
        self.traversable = False

    def contient_teleport(self) -> bool:
        return self.teleport is not None

    def destination_teleport(self):
        if self.contient_teleport():
            return self.teleport
        return None

    def ajouter_teleport(self, destination_name:str, destination_coord:tuple):
        self.teleport = [destination_name,
                         destination_coord[0],
                         destination_coord[1]]

    def ajouter_marchand(self, marchand: Marchand):
        self.marchand = marchand
        self.traversable == False

    def contient_marchand(self) -> bool:
        return self.marchand is not None

    def __str__(self) -> str:
        txt = self.terrain + ":\t"
        if self.traversable:
            txt += "Est traversable"
        else:
            txt += "N’est pas traversable"
        if self.couche2_id is not None:
            txt += "\n" + self.couche2_id
        if self.contient_coffre():
            txt += "\nCette tuile contient un coffre."
        return txt

    def __repr__(self):
        return self.couche1_id

    def rendre_traversable(self):
        self.traversable = True

    def rendre_inaccessible(self):
        self.traversable = False