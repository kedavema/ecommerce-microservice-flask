
# Entidad representando a una Empresa.

class Seller():

    def __init__(self, id, name, short_desc, warehouse, vendedor):

        self.id = id
        self.name = name
        self.short_desc = short_desc
        self.warehouse = warehouse
        self.vendedor = vendedor

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "name": self.name,
            "short_desc": self.short_desc,
            "warehouse": self.warehouse,
            "vendedor": self.vendedor,
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

        id = dict.get("id")
        name = dict.get("name")
        short_desc = dict.get("short_desc")
        warehouse = dict.get("warehouse")
        vendedor = dict.get("vendedor")

        return Seller(id, name, short_desc, warehouse, vendedor)
      