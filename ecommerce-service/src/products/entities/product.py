
# Entidad representando a un producto.

class Product():

    def __init__(self, id, name, short_desc, qty):

        self.id = id
        self.name = name
        self.short_desc = short_desc
        self.qty = qty

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "name": self.name,
            "short_desc": self.short_desc,
            "qty": self.qty,
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
        qty = dict.get("qty")

        return Product(id, name, short_desc, qty)