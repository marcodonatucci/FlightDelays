from database.DB_connect import DBConnect
from model.airport import Airport
from model.edge import Edge


class DAO:

    @staticmethod
    def getAllAirports(min):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.* 
FROM airports a , flights f , airlines a2 
WHERE (a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID) and f.AIRLINE_ID = a2.ID 
GROUP BY a.ID
HAVING COUNT(DISTINCT a2.ID) >=  %s"""

        cursor.execute(query, (min,))

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(min, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, COUNT(*) 
FROM flights f 
WHERE f.ORIGIN_AIRPORT_ID IN (SELECT a.ID 
FROM airports a , flights f , airlines a2 
WHERE (a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID) and f.AIRLINE_ID = a2.ID 
GROUP BY a.ID
HAVING COUNT(DISTINCT a2.ID) >=  %s) AND f.DESTINATION_AIRPORT_ID IN (SELECT a.ID 
FROM airports a , flights f , airlines a2 
WHERE (a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID) and f.AIRLINE_ID = a2.ID 
GROUP BY a.ID
HAVING COUNT(DISTINCT a2.ID) >=  %s) 
GROUP BY f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID """

        cursor.execute(query, (min, min))

        for row in cursor:
            result.append(Edge(idMap[row['ORIGIN_AIRPORT_ID']], idMap[row['DESTINATION_AIRPORT_ID']], row['COUNT(*)']))
        cursor.close()
        conn.close()
        return result


