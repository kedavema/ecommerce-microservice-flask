from src.products.entities.product import Product

# Casos de uso para el manejo de productos.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageProductsUsecase:

    def __init__(self, products_repository):
        self.products_repository = products_repository

    def get_products(self):

        # Retorna una lista de entidades Product desde el repositorio.

        return self.products_repository.get_products() 

    def get_product(self, product_id):

        # Retorna una instancia de Product según la ID recibida.

        return self.products_repository.get_product(product_id)

    def create_product(self, data):

        # Crea una instancia Product desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        product = Product.from_dict(data)
        product = self.products_repository.create_product(product)

        return product

    def update_product(self, product_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        product = self.get_product(product_id)

        if product:

            product = self.products_repository.update_product(product_id, data)

            return product

        else:
            raise ValueError(f"Product of ID {product_id} doesn't exist.")

    def delete_product(self, product_id):

        # Realiza un hard-delete del producto con la ID especificada, si es que existe.

        product = self.get_product(product_id)
        
        if product:

            product = self.products_repository.hard_delete_product(product_id)

        else:
            raise ValueError(f"Product of ID {product_id} doesn't exist or is already deleted.")
          
          
    def decrease_qty(self, product_id, product_qty):
      
        # Disminuye los productos de la db de acuerdo a la cantidad de productos de la orden de compra.
        
        product = self.get_product(product_id)
        
        if product:
            product = self.products_repository.decrease_qty(product_id, product_qty)
          
        else:
            raise ValueError(f"Product of ID {product_id} doesn't exist or is already deleted.")
          
          
    def increase_qty(self, product_id, product_qty):
      
        # Aumenta los productos en la db de acuerdo a la cantidad de productos de la orden de compra cancelada.
        
        product = self.get_product(product_id)
        
        if product:
            product = self.products_repository.increase_qty(product_id, product_qty)
          
        else:
            raise ValueError(f"Product of ID {product_id} doesn't exist or is already deleted.")
          