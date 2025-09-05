import json
from collections import defaultdict
from back_perso import *

def charger_tous_les_objets():
    """Fonction qui charge le contenu complet du fichier JSON contenant l'intégralité des
    objets disponibles et qui retourne un"""
    with open('datas/data_objets.json', 'r', encoding="UTF-8") as fichier:
        return json.load(fichier)

class Objet:
    def __init__(self, objet_id):
        datas = charger_tous_les_objets()
        self.id = objet_id
        self.nom = datas[self.id]["Nom"]
        self.prix = datas[self.id]["Prix"]
        self.vie = datas[self.id]["Vie"]
        self.mana = datas[self.id]["Mana"]
        self.status = datas[self.id]["Status"]
        self.force = datas[self.id]["Force"]
        self.icon = "art/icons/" + datas[self.id].get("Icon", "default_icon.png")


    def __str__(self) -> str:
        txt = self.nom + ":\n"
        txt += f"\tPrix:{self.prix}\n"
        txt += f"\tRedonne {self.vie}PV et {self.mana}PM"
        return txt

    def __getitem__(self, index):
        return self.tab[index]

    def __repr__(self):
        return self.nom

    @property
    def prix_achat(self) -> int:
        return self.prix

    @property
    def prix_vente(self) -> int:
        return int(self.prix_achat * 0.75)

    @property
    def est_equipement(self) -> bool:
        if self.force > 0 :
            return True
        else:
            return False

    @property
    def est_consommable(self) -> bool:
        if self.vie == 0 and self.vie == 0 and self.status == None :
            return False
        else:
            return True

    def inflation(self, taux : int):
        coeff = (1 + taux/100)
        self.prix = int(self.prix * coeff)

    def utiliser(self, perso: Perso):  # New method for using items on slugs.
        if self.est_consommable:  # Check if item *can* be used this way to restore PV or else raise error if invalid.
            if perso.pv < perso.pvMax:  # Check if not already full HP.
                soin = min(self.vie, perso.pvMax - perso.pv)  # Calculate amount to heal (up to max HP)
                perso.pv += soin  # Apply healing
                return f"{perso.nom} a récupéré {soin} PV !"  # Success message
            else:  # Handle already full HP
                return f"{perso.nom} a déjà tous ses PV."
        else:
            return "Cet objet n'est pas utilisable sur un slug."  # Error message if not consumable


class Inventaire:
    def __init__(self):
        # self.tab = []
        self.tab = defaultdict(int)
        self.or_disponible = 0
        #self.or_disponible = sauvegarde["or", 0]

    """def __str__(self) -> str:
        noms_objets = [obj.nom for obj in self.tab]  # Use a list comprehension for clarity
        return ", ".join(noms_objets) if noms_objets else "Vide"""

    # A CHANGER
    def __str__(self) -> str:
        # Format the inventory string with counts
        items_with_counts = []
        for obj_id, count in self.tab.items():
            obj = Objet(obj_id)  # Create Objet instance to get name
            items_with_counts.append(f"{obj.nom} (x{count})")  # Format name (xCount)
        return ", ".join(items_with_counts) if items_with_counts else "Vide"

    """def ajouter(self, liste_objets: list):
        for objet in liste_objets:
            self.tab.append(objet)"""

    # A CHANGER
    def ajouter(self, liste_objets):
        for objet in liste_objets:
            self.tab[objet.id] += 1

    def get(self, i: int) -> Objet:
        return self.tab[i]

    """def enlever(self, i: int) -> Objet:
        self.tab.pop(i)"""

    def enlever(self, objet: Objet):
        if self.tab[objet.id] > 0:
            self.tab[objet.id] -= 1
            if self.tab[objet.id] == 0:
                del self.tab[objet.id]
        else:
            print("L'objet n'est pas dans l'inventaire.")

    def echanger(self, i: int, j: int):
        self.tab[i], self.tab[j] = self.tab[j], self.tab[i]



    def rechercher(self, obj_id: str) -> int:
        for i in range(len(self.tab)):
            if Objet == self.tab[i]:
                return i
        return -1


    def compter(self, obj_id: str) -> int:
        compteur = 0
        for item in self.tab:
            if obj_id == item.couche1_id:
                compteur += 1
        return compteur

    def lister_equipements(self) -> list:
        res = []
        for item in self.tab:
            if item.est_equipement:
                res.append(item)
        return res

    def lister_consommables(self) -> list:
        res = []
        for item in self.tab:
            if item.est_consommable:
                res.append(item)
        return res

    def __len__(self) -> int:
        return len(self.tab)

    def __iter__(self):
        return iter(self.tab)

    def gagner_or(self, montant: int):
        if montant >= 0:
            self.or_disponible += montant
        else:
            raise ValueError("Le montant à ajouter doit être positif.")

    def depenser_or(self, montant: int) -> bool:
        if montant < 0:
            raise ValueError("Le montant à dépenser doit être positif.")
        if montant > self.or_disponible:
            #raise ValueError("Fonds insuffisants pour cette dépense.")
            return False
        else:
            self.or_disponible -= montant
            return True

    def acheter(self, obj: Objet) -> bool:
        if self.or_disponible >= obj.prix_achat:
            self.depenser_or(obj.prix_achat)
            self.tab.append(obj)
            return True
        return False

    def utiliser_objet(self, index_objet: int, perso: Perso) -> str:
        """Utilise l'objet à l'index donné sur le personnage spécifié."""
        try:
            if index_objet >= 0 and index_objet < len(
                    self.tab.keys()):
                obj_id = list(self.tab.keys())[index_objet]
                if obj_id:
                    obj = Objet(obj_id)
                    resultat = obj.utiliser(perso)
                    self.enlever(
                        obj)
                    return resultat
                else:
                    return "Objet invalide."
            else:
                return "Index d'objet invalide."  # Improved message.
        except IndexError:  # Handle case where listbox hasn't finished populating yet if applicable.
            return "Index d'objet invalide ou liste non initialisée."



if __name__ == "__main__":
    item1 = Objet("ITEM_POTION1")
    item2 = Objet("ITEM_SWORD1")
    tab = [item1, item2]
    inv1 = Inventaire()
    inv1.ajouter(tab)
    inv1.gagner_or(100)
    inv1.depenser_or(50)
    print(inv1)

    inv = Inventaire()
    inv.gagner_or(100)
    print("Or disponible avant l'achat :", inv.or_disponible)

    potion = Objet("ITEM_POTION1")
    if inv.acheter(potion):
        print("Achat réussi :", potion)
    else:
        print("Achat échoué : fonds insuffisants.")

    print("Or disponible après l'achat :", inv.or_disponible)
    print("Inventaire :", inv)

