import json

def charger_tous_les_sorts():
    """
    Charge les données de tous les sorts à partir d'un fichier JSON.

    :return: Un dictionnaire contenant les données de tous les sorts.
    :rtype: dict
    """
    try:
        fichier = open(file="datas/data_####.json", mode="r")
        mesDonnees = json.load(fichier)
        fichier.close()
        return mesDonnees
    except FileNotFoundError:
        print("Le fichier datas/data_####.json n'a pas été trouvé.")
        return {}
    except json.JSONDecodeError:
        print("Erreur de décodage JSON dans le fichier datas/data_####.json.")
        return {}


class Magie:
    """
    Représente un sortilège avec ses différentes caractéristiques.

    TODO:
    *   Transformer les fonctions nom, mana, force, vie en attributs de la classe Magie.
    """
    def __init__(self, magie_id:str):
        """
        Initialise un objet Magie.

        :param magie_id: L'identifiant unique du sortilège.
        :type magie_id: str
        """
        # ... (Implémentation manquante)
        # TODO : Charger les données du sortilège à partir de magie_id
        # et les stocker comme attributs de l'objet.
        # Exemple :
        # sort_data = charger_tous_les_sorts()[magie_id]
        # self.nom = sort_data["nom"]
        # self.mana = sort_data["mana"]
        # ...
        pass

        """"
            Exemple de format des données JSON :
            {
            "nom": "Soin mineur",
            "mana": 5,
            "force": 0,
            "vie": 10,
            "retire_status": null,
            "inflige_status": null,
            "icon": ""
            }
        """

    # TODO : À transformer en attributs
    def nom(self, sort: dict) -> str:
        """
        Retourne le nom d'un sortilège.

        :param sort: Un dictionnaire représentant un sortilège.
        :type sort: dict
        :return: Le nom du sortilège.
        :rtype: str
        """
        return sort["nom"]

    def mana(self, sort: dict) -> int:
        """
        Retourne le coût en mana d'un sortilège.

        :param sort: Un dictionnaire représentant un sortilège.
        :type sort: dict
        :return: Le coût en mana du sortilège.
        :rtype: int
        """
        return sort["mana"]

    def force(self, sort: dict) -> int:
        """
        Retourne la force d'attaque d'un sortilège.

        :param sort: Un dictionnaire représentant un sortilège.
        :type sort: dict
        :return: La force d'attaque du sortilège.
        :rtype: int
        """
        return sort["force"]

    def vie(self, sort: dict) -> int:
        """
        Retourne le nombre de points de vie rendus par un sortilège.

        :param sort: Un dictionnaire représentant un sortilège.
        :type sort: dict
        :return: Le nombre de points de vie rendus par le sortilège.
        :rtype: int
        """
        return sort["vie"]

    # TODO : À transformer en méthode
    def est_amical(self, sort: dict) -> bool:
        """
        Indique si un sortilège est amical (peut être utilisé sur un allié).

        :param sort: Un dictionnaire représentant un sortilège.
        :type sort: dict
        :return: True si le sortilège est amical, False sinon.
        :rtype: bool
        """
        if sort["vie"] > 0:
            return True
        else:
            return False


class Grimoire:
    """
    Représente un grimoire contenant une liste de sorts.

    TODO:
    * Transformer les fonctions oublier en méthode de la classe Grimoire.
    """
    def __init__(self, list_ids:list = None):
        """
        Initialise un objet Grimoire.

        :param list_ids: Une liste d'identifiants de sorts à inclure dans le grimoire.
                         Si None, le grimoire est initialement vide.
        :type list_ids: list, optional
        """
        self.tab = []
        if list_ids is not None:
            for sort_id in list_ids:
                self.apprendre(sort_id)

    def apprendre(self, sort_id: str) -> None:
        """
        Ajoute un sort au grimoire.

        :param sort_id: L'identifiant du sort à apprendre.
        :type sort_id: str
        """
        sort = Magie(sort_id)
        self.tab.append(sort)


    def oublier(self, i: int) -> None:
        """
        Retire un sort du grimoire à une position donnée.

        :param i: L'indice du sort à oublier.
        :type i: int
        :raises IndexError: Si l'indice est hors limites.
        """
        try:
            self.tab.pop(i)
        except IndexError:
            print(f"Erreur : L'indice {i} est hors limites pour le grimoire.")
            raise

    def echanger(self, i: int, j: int) -> None:
        """
        Échange la position de deux sorts dans le grimoire.

        :param i: L'indice du premier sort à échanger.
        :type i: int
        :param j: L'indice du deuxième sort à échanger.
        :type j: int
        :raises IndexError: Si l'un des indices est hors limites.
        """
        try:
            tmp = self.tab[i]
            self.tab[i] = self.tab[j]
            self.tab[j] = tmp
        except IndexError:
            print(f"Erreur : L'un des indices ({i}, {j}) est hors limites pour le grimoire.")
            raise

    def rechercher(self, sort: str) -> int:
        """
        Recherche un sort dans le grimoire par son nom.

        :param sort: Le nom du sort à rechercher.
        :type sort: str
        :return: L'indice du sort dans le grimoire, ou -1 si le sort n'est pas trouvé.
        :rtype: int
        """
        for i in range(len(self.tab)):
            if sort == self.tab[i].nom:  # Assumer que Magie a un attribut nom
                return i
        return -1

    def lister_supports(self, dico_sorts: dict) -> list:
        """
        Retourne une liste des identifiants de sorts de support à partir d'un dictionnaire de sorts.

        :param dico_sorts: Un dictionnaire contenant les données de tous les sorts.
        :type dico_sorts: dict
        :return: Une liste des identifiants des sorts de support.
        :rtype: list
        """
        tab_supports = []
        for sort_id in dico_sorts:
            sort = dico_sorts[sort_id]
            if self.est_amical(sort): # Utilise Magie.est_amical
                tab_supports.append(sort_id)
        return tab_supports

    def lister_attaques(self, dico_sorts: dict) -> list:
        """
        Retourne une liste des identifiants de sorts d'attaque à partir d'un dictionnaire de sorts.

        :param dico_sorts: Un dictionnaire contenant les données de tous les sorts.
        :type dico_sorts: dict
        :return: Une liste des identifiants des sorts d'attaque.
        :rtype: list
        """
        tab_attaques = []
        for sort_id in dico_sorts:
            sort = dico_sorts[sort_id]
            if not self.est_amical(sort):  # Utilise Magie.est_amical
                tab_attaques.append(sort_id)
        return tab_attaques


if __name__ == '__main__':
    # Exemple d'utilisation
    m = Magie("sort_soin_mineur") # Remplace ... par l'ID d'un sort
    g = Grimoire(["sort_soin_mineur", "sort_attaque_feu"]) # Remplace [...] par une liste d'IDs de sorts