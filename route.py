import materiel
import connection
import rapportNiveau
import degradation
from degradation import Degradation
class Route:
# Constructeur
    def __init__(self, id_route, roadno, linkno, largeur, longueur, start_km, end_km, materiel):
        self._id_route = id_route
        self._roadno = roadno
        self._linkno = linkno
        self._largeur = largeur
        self._longueur = longueur
        self._start_km = start_km
        self._end_km = end_km
        self._materiel = materiel
        self._degradations = None

# Encapsulation
    def get_id_route(self):
        return self._id_route
    
    def set_id_route(self, id_route):
        self._id_route = id_route

    def get_roadno(self):
        return self._roadno
    
    def set_roadno(self, roadno):
        self._roadno = roadno

    def get_linkno(self):
        return self._linkno
    
    def set_linkno(self, linkno):
        self._linkno = linkno

    def get_largeur(self):
        return self._largeur
    
    def set_largeur(self, largeur):
        return self._largeur
    
    def get_longueur(self):
        return self._longueur
    
    def set_longueur(self, longueur):
        return self._longueur
    
    def get_start_km(self):
        return self._start_km
    
    def set_start_km(self, start_km):
        return self._start_km
    
    def get_end_km(self):
        return self._end_km
    
    def set_end_km(self, end_km):
        return self._end_km
    
    def get_materiel(self):
        return self._materiel
    
    def set_materiel(self, materiel):
        return self._materiel
    
    def get_degradations(self):
        return self._degradations
    
    def set_degradations(self, degradations):
        self._degradations = degradations
    
# Fonctions de classe

    # centre du point a tracer
    def get_center_degraded_point(self):
        listes = self.get_all_degraded_point()
        resultat = []
        for element in listes:
            latitude = (element[0][0] + element[1][0]) / 2
            longitude = (element[0][1] + element[1][1]) / 2
            resultat.append([latitude, longitude, element[2]])
        return resultat

    # fontion qui retourne tous les routes detruit en point geometrique
    def get_all_degraded_point(self):
        degraded_listes = self.get_degradations()
        resultat = []
        for degraded in degraded_listes:
            resultat.append(degraded.get_degradation_Area())
        return resultat

    def get_route_coordinate(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude, geojson FROM roadCoordinate WHERE gid = " + str(self.get_id_route()))
        coord = cursor.fetchone()
        cursor.close()
        conn.close()
        return coord

    def get_reparation_price(self):
        rapport = rapportNiveau.RapportNiveau.get_rapportNiveau()
        degradations = self.get_degradations()
        somme = 0
        for deg in degradations:
            somme += deg.get_reparation_price(rapport)
        return somme
    
    def get_reparation_duration(self):
        rapport = rapportNiveau.RapportNiveau.get_rapportNiveau()
        degradations = self.get_degradations()
        somme = 0       # en heure
        for deg in degradations:
            somme += deg.get_reparation_duration(rapport)
        return somme


    def load_degradations(self):
        # charge tous les degradations d'une route
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM degradation WHERE idroute = " + str(self.get_id_route()))
        listes = cursor.fetchall()
        degradations = []
        for element in listes:
            degr = degradation.Degradation(element[0], element[1], element[2], element[3])
            degr.set_route(self)
            degradations.append(degr)
        self.set_degradations(degradations)
        conn.close()


    @staticmethod
    def get_route(id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        # prendre le materiaux de ce route
        cursor.execute("SELECT idmateriel FROM RouteDetail WHERE idroute = " + str(id))

        id_materiel = cursor.fetchone()[0]
        mat = materiel.Materiel.get_materiel(id_materiel)

        # creation de l'objet route
        cursor.execute("SELECT * FROM madagascar_roads_version4 WHERE gid = " + str(id))
        element = cursor.fetchone()
        route = Route(element[0], element[2], element[1], element[10], element[5], element[3], element[4], mat)
        route.load_degradations()
        conn.close()
        return route
    
    @staticmethod
    def get_degraded_route():
        conn = connection.get_connection()
        cursor = conn.cursor()
        # prendre le materiaux de ce route
        cursor.execute("SELECT distinct idroute FROM degradation")

        routes = cursor.fetchall()
        listes = []
        for route in routes:
            listes.append(Route.get_route(route[0]))
        return listes


road = Route.get_route(2)
print(road.get_center_degraded_point())