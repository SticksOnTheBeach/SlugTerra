from tkinter import messagebox
from back_perso import *
from back_objet import *
from back_tuile import *
from back_objet import Inventaire
import json
import random
from back_marchands import *


class Game:
    """
    Représente une partie du jeu, gérant la carte, le héros, l'inventaire, et l'équipe.
    """

    def __init__(self, sauvegarde: dict):
        """
        Initialise une nouvelle partie à partir des données de sauvegarde.

        :param sauvegarde: Dictionnaire contenant les données de sauvegarde de la partie,
                          notamment le nom de la carte, la position du héros, l'inventaire, etc.
        :type sauvegarde: dict
        """
        self.nom_carte = sauvegarde["nom"]
        self.position_heros = tuple(sauvegarde["position_heros"])
        self.direction = 0  # Direction initiale du héros (0 = haut, 1 = droite, 2 = bas, 3 = gauche)
        self.nb_pas = 0
        self.nb_pas_avant_combat = 18
        self.carte = []

        # Charger l'inventaire
        self.inventaire = Inventaire()
        inventaire_data = sauvegarde["inventaire"]
        if inventaire_data is not None:
            for id_objet in inventaire_data:
                objet = Objet(id_objet)
                self.inventaire.ajouter([objet])

        self.inventaire.or_disponible = sauvegarde["or"]

        # Charger l'équipe
        self.equipe = Equipe()
        equipe_data = sauvegarde.get("equipe", [])  # Charger l'équipe à partir de la sauvegarde
        for perso_id in equipe_data:
            self.equipe.ajouter(perso_id)

        # Ajouter un personnage par défaut à l'équipe si elle est vide
        if len(self.equipe) == 0:
            self.equipe.ajouter("CHARA_RAMMSTONE")  # Exemple : personnage par défaut

        # Générer la carte
        self.generer_carte(self.nom_carte)

    def generer_carte(self, name: str):
        """
        Génère la carte du jeu à partir d'un fichier JSON.

        :param name: Le nom de la carte à charger.
        :type name: str
        """
        self.nom_carte = name
        donnees_carte = charger_carte(self.nom_carte)
        self.carte = []
        for ligne in donnees_carte["Carte"]:
            tab = []
            for dico in ligne:
                couche1_id = dico["couche1_id"]
                couche2_id = dico["couche2_id"]
                tab.append(Tuile(couche1_id, couche2_id))
            self.carte.append(tab)
        if "Monstres" in donnees_carte:
            self.monstres = donnees_carte["Monstres"]
        else:
            self.monstres = []
        self.monstre_choisi = None

        # Chargement des coffres
        for coffre in donnees_carte["Coffres"]:
            position = coffre["position"]
            ligne, col = position
            contenu = coffre["contenu"]
            # Associe un coffre à la tuile correspondante
            if self.position_valide(ligne, col):
                tuile = self.tuile(ligne, col)
                tuile.ajouter_coffre(contenu)

        # Chargement des téléports
        for teleport in donnees_carte["Teleports"]:
            position = teleport["emplacement"]
            ligne, col = position
            carte_cible = teleport["carte_cible"]
            coord_cible = teleport["coordonnees_cibles"]
            # Associe un coffre à la tuile correspondante
            if self.position_valide(ligne, col):
                tuile = self.tuile(ligne, col)
                tuile.ajouter_teleport(carte_cible, coord_cible)

        # Chargement des marchands
        if "Marchands" in donnees_carte.keys():  # Explicitly check for the Marchand key:
            for marchand_data in donnees_carte["Marchands"]:
                position = marchand_data["position"]
                ligne, col = position
                inventaire_marchand = marchand_data["inventaire"]
                if self.position_valide(ligne, col):
                    tuile = self.tuile(ligne, col)
                    tuile.ajouter_marchand(Marchand(inventaire_marchand))
                    # Todo : lorsque la tuile devant le joueur contient un marchands, traversable = False
                    """if self.tuile_devant.contient_marchands(): 
                        self.traversable == False"""

    def choisir_monstre(self) -> tuple:
        """
        Choisit un monstre aléatoire parmi ceux disponibles sur la carte.

        :return: Un tuple contenant l'instance du monstre et l'expérience gagnable pour l'avoir vaincu.
        :rtype: tuple
        """
        monstre_id = random.choice(self.monstres)
        monstre = Perso(monstre_id)

        # Déterminer l'expérience gagnable
        experience_gagnable = 10  # TODO :  FIX : monstre_data["experience", 10]  # Par défaut 10 points d'expérience
        return monstre, experience_gagnable

    def peut_ouvrir_un_coffre(self) -> bool:
        """
        Vérifie s'il y a un coffre devant le héros.

        :return: True si un coffre est présent, False sinon.
        :rtype: bool
        """
        tuile_devant = self.tuile_devant()
        return tuile_devant is not None and tuile_devant.contient_coffre()

    def ouvrir_coffre(self) -> str:
        """
        Ouvre un coffre et récupère son contenu si possible.

        :return: Message décrivant le résultat de l'action.
        :rtype: str
        """
        if self.peut_ouvrir_un_coffre():
            tuile_devant = self.tuile_devant()
            contenu = tuile_devant.ouvrir_coffre()
            if contenu:
                self.inventaire.ajouter(contenu)
                return f"Vous avez récupéré : \n{contenu}"
            else:
                return "Le coffre est vide."
        return "Il n'y a pas de coffre devant vous."

    @property
    def hauteur(self):
        """
        :return: La hauteur de la carte.
        :rtype: int
        """
        return len(self.carte)

    @property
    def largeur(self):
        """
        :return: La largeur de la carte.
        :rtype: int
        """
        return len(self.carte[0])

    @property
    def dimensions(self):
        """
        :return: Les dimensions de la carte sous forme d'un tuple (hauteur, largeur).
        :rtype: tuple
        """
        return self.hauteur, self.largeur

    def tuile(self, ligne: int, col: int) -> Tuile:
        """
        Récupère une tuile à une position donnée sur la carte.

        :param ligne: L'indice de la ligne de la tuile.
        :type ligne: int
        :param col: L'indice de la colonne de la tuile.
        :type col: int
        :return: La tuile à la position spécifiée, ou None si la position est invalide.
        :rtype: Tuile
        """
        if self.position_valide(ligne, col):
            return self.carte[ligne][col]
        return None

    def position_valide(self, ligne: int, col: int) -> bool:
        """
        Vérifie si une position donnée est valide sur la carte.

        :param ligne: L'indice de la ligne de la position.
        :type ligne: int
        :param col: L'indice de la colonne de la position.
        :type col: int
        :return: True si la position est valide, False sinon.
        :rtype: bool
        """
        return 0 <= ligne < self.hauteur and 0 <= col < self.largeur

    def deplacer_gauche(self):
        """Déplace le héros vers la gauche si possible."""
        self.direction = 3
        ligne, col = self.position_heros
        if self.position_valide(ligne, col - 1) and self.carte[ligne][col - 1].traversable:
            self.position_heros = (ligne, col - 1)
            self.nb_pas += 1  # Incrémente le nombre de pas
            self.verifier_teleport()

    def deplacer_droite(self):
        """Déplace le héros vers la droite si possible."""
        self.direction = 1
        ligne, col = self.position_heros
        if self.position_valide(ligne, col + 1) and self.carte[ligne][col + 1].traversable:
            self.position_heros = (ligne, col + 1)
            self.nb_pas += 1  # Incrémente le nombre de pas
            self.verifier_teleport()

    def deplacer_haut(self):
        """Déplace le héros vers le haut si possible."""
        self.direction = 0
        ligne, col = self.position_heros
        if self.position_valide(ligne - 1, col) and self.carte[ligne - 1][col].traversable:
            self.position_heros = (ligne - 1, col)
            self.nb_pas += 1  # Incrémente le nombre de pas
            self.verifier_teleport()

    def deplacer_bas(self):
        """Déplace le héros vers le bas si possible."""
        self.direction = 2
        ligne, col = self.position_heros
        if self.position_valide(ligne + 1, col) and self.carte[ligne + 1][col].traversable:
            self.position_heros = (ligne + 1, col)
            self.nb_pas += 1  # Incrémente le nombre de pas
            self.verifier_teleport()

    def verifier_combat(self) -> bool:
        """
        Vérifie si le nombre de pas effectués atteint le seuil pour un combat.

        :return: True si un combat doit avoir lieu, False sinon.
        :rtype: bool
        """
        if self.nb_pas >= self.nb_pas_avant_combat and len(self.monstres) > 0:
            self.reinitialiser_pas()  # Réinitialise le compteur de pas après le combat
            return True
        return False

    def verifier_teleport(self):
        """Vérifie si le héros se trouve sur une tuile de téléportation et le téléporte si c'est le cas."""
        l, c = self.position_heros
        tuile_actuelle = self.tuile(l, c)
        if tuile_actuelle and tuile_actuelle.contient_teleport():
            name, ligne, col = tuile_actuelle.destination_teleport()
            self.position_heros = ligne, col
            self.nom_carte = name
            self.generer_carte(name)

    def reinitialiser_pas(self):
        """Réinitialise le nombre de pas effectués."""
        self.nb_pas = 0

    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de la carte.

        :return: Une chaîne de caractères représentant la carte.
        :rtype: str
        """
        Game_str = ""
        for ligne in range(self.hauteur):
            for col in range(self.largeur):
                if (ligne, col) == self.position_heros:
                    Game_str += "H "
                else:
                    Game_str += self.carte[ligne][col].terrain[0] + " "
            Game_str += "\n"
        return Game_str

    def alentours(self):
        """
        Récupère les tuiles autour du héros.

        :return: Une liste de listes représentant les tuiles autour du héros.
        :rtype: list
        """
        ligne, col = self.position_heros
        alentours = []
        for i in range(ligne - 5, ligne + 6):
            ligne_alentours = []
            for j in range(col - 7, col + 8):
                if self.position_valide(i, j):
                    ligne_alentours.append(self.carte[i][j])
                else:
                    ligne_alentours.append(None)
            alentours.append(ligne_alentours)
        return alentours

    def tuile_devant(self):
        """
        Retourne la tuile devant le héros en fonction de sa direction.
        Renvoie None si la case est hors de la carte.

        :return: La tuile devant le héros, ou None si elle est hors de la carte.
        :rtype: Tuile or None
        """
        ligne, col = self.position_heros
        if self.direction == 0:  # Haut
            ligne -= 1
        elif self.direction == 1:  # Droite
            col += 1
        elif self.direction == 2:  # Bas
            ligne += 1
        elif self.direction == 3:  # Gauche
            col -= 1

        # Vérifie si la case est hors de la carte
        if 0 <= ligne < self.hauteur and 0 <= col < self.largeur:
            return self.carte[ligne][col]  # Retourne la tuile à la position calculée
        return None  # Retourne None si la position est hors de la carte

    def interagir_marchand(self):
        """
        Retourne le marchand sur la tuile devant le héros, si présent.

        :return: Le marchand sur la tuile devant le héros, ou None s'il n'y en a pas.
        :rtype: Marchand or None
        """
        tuile_devant = self.tuile_devant()
        if tuile_devant is not None and tuile_devant.contient_marchand():
            return tuile_devant.marchand
        return None

    def ajouter_objet(self, objet):
        """
        Ajoute un objet à l'inventaire du joueur et sauvegarde la partie.

        :param objet: L'objet à ajouter à l'inventaire.
        :type objet: Objet
        """
        self.inventaire.ajouter(objet)
        self.sauvegarder_partie()  # Sauvegarder immédiatement après ajout

    def retirer_objet(self, objet):
        """
        Retire un objet de l'inventaire du joueur et sauvegarde la partie.

        :param objet: L'objet à retirer de l'inventaire.
        :type objet: Objet
        """
        self.inventaire.enlever(objet)
        self.sauvegarder_partie()  # Sauvegarder immédiatement après suppression

    def sauvegarder_partie(self, filename: str):
        """Sauvegarde l'état de la partie dans un fichier JSON."""
        # Création d'un tableau d'identifiant à partir de l'inventaire
        inventaire_sauvegarde = []
        for obj_id, count in self.inventaire.tab.items():
            for _ in range(count):
                inventaire_sauvegarde.append(obj_id)
        # Création d'un dictionnaire pour la sauvegarde
        sauvegarde = {
            "nom": self.nom_carte,
            "position_heros": self.position_heros,
            "or": self.inventaire.or_disponible,
            "inventaire": inventaire_sauvegarde,
            "equipe": [perso.id for perso in self.equipe],
            "nb_pas": self.nb_pas,
        }
        # Enregistrement des données
        with open(f"saves/{filename}.json", "w") as fichier:
            json.dump(sauvegarde, fichier, indent=4)
        print("La partie a été sauvegardée dans", filename, ".json")


# ---------------------------------------------------------------------------------

def charger_carte(filename: str):
    """Charge les données de la carte ou de l'état du jeu depuis un fichier."""
    try:
        with open(f"maps/{filename}.json", "r") as file:
            donnees = json.load(file)  # Charge les données depuis un fichier JSON
        return donnees  # Renvoie les données du jeu
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {filename}: {e}")
        return None


def charger_partie(filename: str) -> Game:
    """
    Charge une partie sauvegardée à partir d'un fichier JSON.

    :param filename: Le nom du fichier de sauvegarde à charger.
    :type filename: str
    :return: Une instance de la classe Game initialisée avec les données de sauvegarde.
    :rtype: Game
    """
    with open(f"saves/{filename}.json", "r", encoding="utf8") as fichier:
        sauvegarde = json.load(fichier)
    return Game(sauvegarde)

