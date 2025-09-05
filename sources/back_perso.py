import json


def charger_tous_les_characters():
    """
    Charge les données de tous les personnages depuis un fichier JSON.

    :return: Un dictionnaire contenant les données de tous les personnages,
             où les clés sont les IDs des personnages et les valeurs sont
             des dictionnaires contenant leurs données.
    :rtype: dict
    """
    try:
        fichier = open(file="datas/data_characters.json", mode="r")
        mesDonnees = json.load(fichier)
        fichier.close()
        return mesDonnees
    except FileNotFoundError:
        print("Le fichier datas/data_characters.json n'a pas été trouvé.")
        return {}
    except json.JSONDecodeError:
        print("Erreur de décodage JSON dans le fichier datas/data_characters.json.")
        return {}


class Perso:
    """
    Représente un personnage avec ses différentes caractéristiques.
    """

    def __init__(self, perso_id: str):
        """
        Initialise un objet Perso (personnage).

        :param perso_id: L'identifiant unique du personnage.
        :type perso_id: str
        """
        datas = charger_tous_les_characters()
        self.id = perso_id
        self.nom = datas[self.id]["nom"]
        self.pvMax = datas[self.id]["vie"]
        self.pv = self.pvMax
        self.pmMax = datas[self.id]["mana"]
        self.pm = self.pmMax
        self.force = datas[self.id]["force"]
        self.magie = datas[self.id]["magie"]
        self.icon = "art/faces/" + datas[self.id]["portrait"]
        self.status = None
        self.experience = 0
        self.grimoire = datas[self.id].get("sorts")  # Peut être None

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle du personnage.

        :return: Une chaîne de caractères représentant le personnage
                 avec ses statistiques principales.
        :rtype: str
        """
        txt = self.nom + ":\n"
        txt += f"\tPV :{self.pv}/{self.pvMax}\n"
        txt += f"\tPM :{self.pm}/{self.pmMax}\n"
        txt += f"\tATT :{self.force}\n"
        txt += f"\tMAG :{self.magie}\n"
        txt += f"\tEXP :{self.experience}"
        return txt

    def est_mort(self) -> bool:
        """
        Vérifie si le personnage est mort.

        :return: True si les points de vie (PV) du personnage sont inférieurs
                 ou égaux à zéro, False sinon.
        :rtype: bool
        """
        return self.pv <= 0

    def peut_utiliser_magie(self) -> bool:
        """
        Vérifie si le personnage a suffisamment de points de magie (PM)
        pour lancer un sort.

        :return: True si les points de magie (PM) du personnage sont
                 strictement supérieurs à zéro, False sinon.
        :rtype: bool
        """
        return self.pm > 0

    def gagner_experience(self, points: int):
        """
        Augmente l'expérience du personnage.

        :param points: Le nombre de points d'expérience à ajouter.
        :type points: int
        :raises ValueError: Si les points sont négatifs.
        """
        if points < 0:
            raise ValueError("Les points d'expérience ne peuvent pas être négatifs.")
        self.experience += points

    @property
    def est_vivant(self) -> bool:
        """
        Vérifie si le personnage est vivant. (Propriété)

        :return: True si les points de vie (PV) du personnage sont
                 strictement supérieurs à zéro, False sinon.
        :rtype: bool
        """
        return self.pv > 0

    def blesser(self, degats: int) -> int:
        """
        Réduit les points de vie du personnage.

        :param degats: Le nombre de points de dégâts à infliger.
        :type degats: int
        :return: Le nombre de points de dégâts infligés (peut être différent
                 si les PV tombent en dessous de zéro).
        :rtype: int
        """
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0
        return degats

    def soigner(self, value: int) -> str:
        """
        Augmente les points de vie du personnage.

        :param value: Le nombre de points de vie à ajouter.
        :type value: int
        :return: Un message indiquant le nombre de PV gagnés.
        :rtype: str
        """
        self.pv += value
        if self.pv > self.pvMax:
            self.pv = self.pvMax
        return f"{self.nom} gagne {value} PV"

    def frapper(self, other: 'Perso') -> str:
        """
        Fait attaquer le personnage courant un autre personnage.

        :param other: Le personnage à attaquer (instance de la classe Perso).
        :type other: Perso
        :return: Un message décrivant l'attaque et les dégâts infligés.
        :rtype: str
        """
        degats = self.force
        other.blesser(degats) # Applique les dégâts en utilisant la méthode blesser
        if other.pv >= 0:
            return f"{self.nom} attaque {other.nom} et inflige {degats} points de dégâts."
        else:
            other.pv = 0
            return f"{self.nom} a tué {other.nom}"

    def lancer_sort(self, spell_name: str, other: 'Perso') -> str:
        """
        Fait lancer un sort par le personnage.

        :param spell_name: Le nom du sort à lancer.
        :type spell_name: str
        :param other: Le personnage ciblé par le sort (instance de la classe Perso).
        :type other: Perso
        :return: Un message décrivant l'effet du sort ou une erreur si le
                 personnage n'a pas assez de PM ou si le sort n'est pas dans
                 son grimoire.
        :rtype: str
        """
        if self.grimoire:  # Vérifie si le grimoire n'est pas None
            for spell in self.grimoire:
                if spell["nom"] == spell_name:
                    if self.pm >= spell["mana"]:
                        self.pm -= spell["mana"]
                        spell_type = spell.get("type", "")
                        if spell_type == "offensif":
                            degats = spell.get("degats", 0)  # Default to 0 if 'degats' is missing
                            other.blesser(degats)
                            return f"{self.nom} lance {spell_name} sur {other.nom} et inflige {degats} dégâts."

                        elif spell_type == "amical":
                            soin = spell.get("soin", 0) # Default to 0 if 'soin' is missing
                            self.soigner(soin)
                            return f"{self.nom} lance {spell_name} et se soigne de {soin} PV."
                        else:
                            return f"Le sort {spell_name} a un type inconnu."
                    else:
                        return "Vous n'avez pas assez de PM pour lancer ce sort."
            return f"Le sort {spell_name} n'est pas dans votre grimoire."
        else:
            return f"{self.nom} n'a pas de grimoire."


class Equipe:
    """
    Représente une équipe de personnages.
    """

    def __init__(self, max_size=4):
        """
        Initialise un objet Equipe.

        :param max_size: La taille maximale de l'équipe (par défaut 4).
        :type max_size: int
        """
        self.tab = []  # Tableau vide pour les membres de l'équipe
        self.max = max_size  # Taille maximale de l'équipe

    def ajouter(self, perso_id: str):
        """
        Ajoute un personnage à l'équipe.

        :param perso_id: L'identifiant unique du personnage à ajouter.
        :type perso_id: str
        """
        perso = Perso(perso_id)
        if len(self.tab) < self.max:
            self.tab.append(perso)

    def get(self, i: int) -> 'Perso':
        """
        Récupère un personnage de l'équipe à un indice donné.

        :param i: L'indice du personnage à récupérer.
        :type i: int
        :return: Le personnage à l'indice donné, ou None si l'indice
                 est hors limites.
        :rtype: Perso or None
        """
        if 0 <= i < len(self.tab):
            return self.tab[i]
        return None

    def enlever(self, i: int) -> 'Perso':
        """
        Retire un personnage de l'équipe à un indice donné.

        :param i: L'indice du personnage à retirer.
        :type i: int
        :return: Le personnage retiré, ou None si l'indice est hors limites.
        :rtype: Perso or None
        """
        if 0 <= i < len(self.tab):
            perso = self.tab[i]
            del self.tab[i]  # Supprime le personnage à l'indice i
            return perso
        return None

    def echanger(self, i: int, j: int):
        """
        Échange la position de deux personnages dans l'équipe.

        :param i: L'indice du premier personnage à échanger.
        :type i: int
        :param j: L'indice du deuxième personnage à échanger.
        :type j: int
        """
        if (0 <= i < len(self.tab)) and (0 <= j < len(self.tab)):
            perso_temp = self.tab[i]
            self.tab[i] = self.tab[j]
            self.tab[j] = perso_temp

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de l'équipe.

        :return: Une chaîne de caractères représentant l'équipe,
                 avec les informations de chaque personnage.
        :rtype: str
        """
        result = ""
        for perso in self.tab:
            result += str(perso) + "\n"
        return result.strip()

    def rechercher(self, perso: 'Perso') -> bool:
        """
        Recherche un personnage dans l'équipe.

        :param perso: Le personnage à rechercher.
        :type perso: Perso
        :return: True si le personnage est trouvé dans l'équipe,
                 False sinon.
        :rtype: bool
        """
        return perso in self.tab

    def compter(self, perso_id: str) -> int:
        """
        Compte le nombre de personnages avec un ID donné dans l'équipe.

        :param perso_id: L'ID du personnage à compter.
        :type perso_id: str
        :return: Le nombre de personnages avec l'ID donné dans l'équipe.
        :rtype: int
        """
        count = 0
        for perso in self.tab:
            if perso.id == perso_id: # Utilisez perso.id pour comparer l'ID du personnage
                count += 1
        return count

    def trier_par_nom(self):
        """Trie l'équipe par nom de personnage."""
        self.tab.sort(key=lambda perso: perso.nom)

    def lister_survivants(self) -> list:
        """
        Retourne une liste des personnages survivants dans l'équipe.

        :return: Une liste des personnages qui sont vivants (PV > 0).
        :rtype: list
        """
        survivants = [perso for perso in self.tab if perso.est_vivant]
        return survivants

    def est_vaincue(self) -> bool:
        """
        Vérifie si l'équipe est vaincue (tous les personnages sont morts).

        :return: True si tous les personnages de l'équipe sont morts,
                 False sinon.
        :rtype: bool
        """
        return all(perso.est_mort() for perso in self.tab)

    def __len__(self) -> int:
        """
        Retourne le nombre de personnages dans l'équipe.

        :return: Le nombre de personnages dans l'équipe.
        :rtype: int
        """
        return len(self.tab)

    def __iter__(self):
        """
        Retourne un itérateur pour parcourir les personnages de l'équipe.

        :return: Un itérateur pour l'équipe.
        :rtype: iterator
        """
        return iter(self.tab)


if __name__ == "__main__":
    equipe = Equipe()
    equipe.ajouter("CHARA_RAMMSTONE")
    equipe.ajouter("CHARA_PEKUN")
    equipe.ajouter("CHARA_INFURNUS")
    print(equipe)
