
# Entidad representando a una orden de compra.

class Order():

    def __init__(self, id, status, product_sku, product_qty, product_name):

        self.id = id
        self.status = status
        self.product_sku = product_sku
        self.product_qty = product_qty
        self.product_name = product_name

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "status": self.status,
            "product_sku": self.product_sku,
            "product_qty": self.product_qty,
            "product_name": self.product_name,
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
        status = dict.get("status")
        product_sku = dict.get("product_sku")
        product_qty = dict.get("product_qty")
        product_name = dict.get("product_name")

        return Order(id, status, product_sku, product_qty, product_name)