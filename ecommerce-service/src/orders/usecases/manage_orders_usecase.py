from src.orders.entities.order import Order
import requests
import json

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

    def create_order(self, order, product, user_id, manage_users_usecase):

        # Crea una instancia Order desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
        
        user = manage_users_usecase.get_user(user_id)
        
        print(user.name, "Este es el usuario")
        
        order["status"] = "created"
        order["product_name"] = product.name
        order["customer_id"] = user_id
        order["customer_address"] = user.shipping_address
            
        order = Order.from_dict(order)
        order = self.orders_repository.create_order(order)

        return order

    def change_order_status(self, order_id, fields, manage_products_usecase, manage_users_usecase):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        order = self.get_order(order_id)
        costumer = manage_users_usecase.get_user(order.customer_id)

        if order:
          
            if fields["status"] == "confirmed":
              
                # Si el estado es cambiado a Confirmado, el producto 
                # que se obtiene de la orden de compra se reduce de la base de datos.
              
                order = self.orders_repository.change_order_status(order_id, fields)
                manage_products_usecase.decrease_qty(order.product_sku, order.product_qty)
                
                return order
              
            elif fields["status"] == "dispatched":
              
                # Si el estado es cambiado a enviado, se crea una orden de compra enviando
                # los datos al endpoint de deliveries.
              
                data = {
                    "order":
                    {
                        "foreing_order_id": order.id,
                        "products": [{
                                "sku": order.product_sku,
                                "name": order.product_name,
                                "qty": order.product_qty
                            }]
                    },
                    "origin": {
                        "address": "warehouse address"
                    },
                    "destination": {
                        "name": costumer.name,
                        "address": costumer.shipping_address
                    }
                }
              
                url = "http://host.docker.internal:8001/deliveries"
                headers = {"Content-Type": "application/json"}
                session = requests.Session()
                session.post(url, data=json.dumps(data), headers=headers)
                
                order = self.orders_repository.change_order_status(order_id, fields)
                
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