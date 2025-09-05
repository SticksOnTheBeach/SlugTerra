from back_objet import Inventaire, Objet

class Marchand:
    """
    Représente un marchand avec un inventaire d'objets à vendre.
    """

    def __init__(self, inventaire_ids: list):
        """
        Initialise un marchand avec un inventaire basé sur une liste d'identifiants d'objets.

        :param inventaire_ids: Une liste d'identifiants d'objets à ajouter à l'inventaire du marchand.
        :type inventaire_ids: list
        """
        self.inventaire = Inventaire()
        for objet_id in inventaire_ids:
            self.inventaire.ajouter([Objet(objet_id)])