CREATE TABLE Materiel (
    idMateriel SERIAL PRIMARY KEY,
    nom VARCHAR(20),
    prixUnitaire FLOAT,
    duree FLOAT
);

CREATE TABLE RouteDetail (
    idRoute SERIAL,
    idMateriel SERIAL,
    FOREIGN KEY(idRoute) REFERENCES madagascar_roads_version4,
    FOREIGN KEY(idMateriel) REFERENCES Materiel
);

CREATE TABLE Degradation (
    idDegradation SERIAL PRIMARY KEY,
    pkDebut INTEGER,
    pkFin INTEGER,
    niveau INTEGER,
    idRoute SERIAL,
    FOREIGN KEY(idRoute) REFERENCES madagascar_roads_version4
);

CREATE TABLE RapportNiveau (
    niveau INTEGER,
    profondeur FLOAT
);

CREATE VIEW RoadCoordinate AS
SELECT gid, ST_X(ST_StartPoint(geom)) as latitude, ST_Y(ST_StartPoint(geom)) as longitude, ST_AsGeoJSON(geom) as geoJSON 
FROM "public"."madagascar_roads_version4";

-- Insertion des donnees de test
INSERT INTO Materiel VALUES (DEFAULT, 'Goudron', 100, 5);
INSERT INTO Materiel VALUES (DEFAULT, 'Pave', 30, 3);

INSERT INTO RapportNiveau VALUES (100, 50);

-- Je vais travailler avec les routes de RN2 : 2  RNP_2_06_1 | 79 RNP_2_09_2_a | 199 RNP_2_06_3
INSERT INTO Degradation VALUES (DEFAULT, 110, 120, 8, 2);
INSERT INTO Degradation VALUES (DEFAULT, 120, 125, 5, 2);

INSERT INTO Degradation VALUES (DEFAULT, 290, 295, 12, 79);

INSERT INTO Degradation VALUES (DEFAULT, 178, 180, 7, 199);

INSERT INTO RouteDetail VALUES (2, 1);
INSERT INTO RouteDetail VALUES (79, 1);
INSERT INTO RouteDetail VALUES (199, 2);