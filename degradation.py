import connection
from map import getPointCoordonnee
class Degradation:
# Constructeur
    def __init__(self, id_degradation, pk_debut, pk_fin, niveau):
        self._id_degradation = id_degradation
        self._pk_debut = pk_debut
        self._pk_fin = pk_fin
        self._niveau = niveau
        self._route = None

# Encapsulation
    def get_id_degradation(self):
        return self._id_degradation
    
    def set_id_degradation(self, id_degradation):
        self._id_degradation = id_degradation

    def get_pk_debut(self):
        return self._pk_debut
    
    def set_pk_debut(self, pk_debut):
        self._pk_debut = pk_debut

    def get_pk_fin(self):
        return self._pk_fin
    
    def set_pk_fin(self, pk_fin):
        self._pk_fin = pk_fin

    def get_niveau(self):
        return self._niveau
    
    def set_niveau(self, niveau):
        self._niveau = niveau

    def get_route(self):
        return self._route
    
    def set_route(self, route):
        self._route = route

# Fonction de classe
    def get_degradation_Area(self):
        coordDebut = getPointCoordonnee(self.get_route().get_linkno(), self.get_pk_debut())
        coordFin = getPointCoordonnee(self.get_route().get_linkno(), self.get_pk_fin())
        rayon = ((self.get_pk_fin() - self.get_pk_debut()) * 1000) / 2
        return [coordDebut, coordFin, rayon]

    def get_reparation_price(self, rapport):
        longueur = self.get_pk_fin() - self.get_pk_debut()
        largeur = self.get_route().get_largeur()
        profondeur = (self.get_niveau() * rapport.get_profondeur()) / rapport.get_niveau() # en cm
        prix_unitaire = self.get_route().get_materiel().get_prix_unitaire()
        return longueur * largeur * (profondeur / 100) * prix_unitaire
    
    def get_reparation_duration(self, rapport):
        longueur = self.get_pk_fin() - self.get_pk_debut()
        largeur = self.get_route().get_largeur()
        profondeur = (self.get_niveau() * rapport.get_profondeur()) / rapport.get_niveau() # en cm
        temps_m = self.get_route().get_materiel().get_duree()
        return longueur * largeur * (profondeur / 100) * temps_m
    
    @staticmethod
    def get_all_degradation():
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM degradation")
        listes = cursor.fetchall()
        degradations = []
        for element in listes:
            degradations.append(Degradation(element[0], element[1], element[2], element[3]))
        conn.close()
        return degradations

    @staticmethod
    def get_degradation(id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM degradation WHERE iddegradation = " + str(id))
        listes = cursor.fetchone()
        conn.close()
        return Degradation(listes[0], listes[1], listes[2], listes[3])

