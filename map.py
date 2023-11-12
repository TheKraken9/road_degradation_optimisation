import connection

def getPointCoordonnee(linkno, pk):    # distance en km
    conn = connection.get_connection()
    cursor = conn.cursor()

    # Prends la distance en km du pk et du point depart
    sql = "select {} - start_km from madagascar_roads_version4 where linkno = '{}'".format(pk, linkno)
    cursor.execute(sql)
    distance = cursor.fetchone()[0]

    # Prends la distance en km de la longueur de la route
    sql = "select ST_Length(geom::geography) / 1000 from madagascar_roads_version4 where linkno = '{}'".format(linkno)
    cursor.execute(sql)
    total = cursor.fetchone()[0]

    # Prends le point au pk donnée
    sql = "select ST_X(ST_LineInterpolatePoint(st_makeline(st_linemerge(geom)), {} / {})) as latitude, ST_Y(ST_LineInterpolatePoint(st_makeline(st_linemerge(geom)), {} / {})) as longitude from madagascar_roads_version4 where linkno = '{}'".format(distance, total, distance, total, linkno)
    cursor.execute(sql)
    point = cursor.fetchone()

    cursor.close()
    conn.close()
    return point