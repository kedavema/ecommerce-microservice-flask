
# Entidad representando a un Usuario.

class User():

    def __init__(self, id, name, password, email, shipping_address, is_superuser = False, is_seller = False):

        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.shipping_address = shipping_address
        self.is_superuser = is_superuser
        self.is_seller = is_seller
        
    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "email": self.email,
            "shipping_address": self.shipping_address,
            "is_superuser": self.is_superuser,
            "is_seller": self.is_seller,
        }

    def serialize(self):

        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()
        
        return data

    @classmethod
    def from_dict(cls, dict):

        # Retorna una instancia de este objeto desde un diccionario de datos,
        # para no tener que llamar al constructor pasando los datos uno a uno.
        # Si un campo falta en el diccionario, se asume valor None.

        id = dict.get("id")
        name = dict.get("name")
        password = dict.get("password")
        email = dict.get("email")
        shipping_address = dict.get("shipping_address")
        is_superuser = dict.get("is_superuser")
        is_seller = dict.get("is_seller")

        return User(id, name, password, email, shipping_address, is_superuser, is_seller)