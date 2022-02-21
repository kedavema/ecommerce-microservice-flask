from src.orders.entities.order import Order

# Casos de uso para el manejo de Ordenes de compra.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageOrdersUsecase:

    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def get_orders(self):

        # Retorna una lista de entidades Order desde el repositorio.

        return self.orders_repository.get_orders() 

    def get_order(self, order_id):

        # Retorna una instancia de Order según la ID recibida.

        return self.orders_repository.get_order(order_id)

    def create_order(self, data):

        # Crea una instancia Order desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        order = Order.from_dict(data)
        order = self.orders_repository.create_order(order)

        return order

    def change_order_status(self, order_id, fields, manage_products_usecase):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        order = self.get_order(order_id)

        if order:
            if fields["status"] == "confirmed":
              
                # Si el estado es cambiado a Confirmado, el producto 
                # que se obtiene de la orden de compra se reduce de la base de datos.
              
                order = self.orders_repository.change_order_status(order_id, fields)
                manage_products_usecase.decrease_qty(order.product_sku, order.product_qty)
                
                return order
              
            else:
                order = self.orders_repository.change_order_status(order_id, fields)

                return order

        else:
            raise ValueError(f"Order of ID {order_id} doesn't exist.")

    def cancel_order(self, order_id, manage_products_usecase):

        # Realiza una cancelación de la orden con la ID especificada, si es que existe.

        order = self.get_order(order_id)
        
        if order:
            if order.status == "created" or order.status == "confirmed":
                # Aquí recuperamos la cantidad disminuida al confirmar la orden de compra.
                manage_products_usecase.increase_qty(order.product_sku, order.product_qty)
                # Eliminamos la orden de compra.
                order = self.orders_repository.cancel_order(order_id)
          
            else:
                raise ValueError("To cancel an order the status must be created or confirmed")
            
        else:
            raise ValueError(f"Order of ID {order_id} doesn't exist or is already cancelled.")