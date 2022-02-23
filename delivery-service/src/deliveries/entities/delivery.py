
# Entidad representando a un Delivery.

class Delivery():

    def __init__(self, tracking_number, order, origin, destination, status, tracking):

        # self.id = id
        self.tracking_number = tracking_number
        self.order = order
        self.origin = origin
        self.destination = destination
        self.status = status
        self.tracking = tracking

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            # "id": self.id,
            "tracking_number": self.tracking_number,
            "order": self.order,
            "origin": self.origin,
            "destination": self.destination,
            "status": self.status,
            "tracking": self.tracking,
        }

    def serialize(self):

        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.

        data = self.to_dict()
        
        return data

    @classmethod
    def from_dict(cls, dict):

        # Retorna una instancia de este objeto desde un diccionario de datos,
        # para no tener que llamar al constructor pasando los datos uno a uno.
        # Si un campo falta en el diccionario, se asume valor None.

        # id = dict.get("id")
        tracking_number = dict.get("tracking_number")
        order = dict.get("order")
        origin = dict.get("origin")
        destination = dict.get("destination")
        status = dict.get("status")
        tracking = dict.get("tracking")

        return Delivery(tracking_number, order, origin, destination, status, tracking)