from .entities.Location import Location
class ModelLocation():

    @classmethod
    def consultAll(self, db):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, nombre FROM ubicaciones";
            cursor.execute(sql)
            list_locations=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_locations.append( Location(id=row[0], nombre=row[1]))
            
            if len(list_locations)>0:
                return list_locations
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    