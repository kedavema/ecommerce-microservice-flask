from src.deliveries.entities.delivery import Delivery

from src.utils.utils import get_current_datetime, format_date

# Casos de uso para el manejo de Deliveries.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageDeliveriesUsecase:

    def __init__(self, deliveries_repository):
        self.deliveries_repository = deliveries_repository

    def get_deliveries(self):

        # Retorna una lista de entidades delivery desde el repositorio.

        return self.deliveries_repository.get_deliveries() 

    def get_delivery(self, delivery_id):

        # Retorna una instancia de delivery según la ID recibida.

        return self.deliveries_repository.get_delivery(delivery_id)
      
    def get_delivery_tracking(self, tracking_number):

        # Retorna una instancia de delivery según la ID recibida.

        delivery = self.deliveries_repository.get_delivery_tracking(tracking_number)
        data = {
          "tracking_number": delivery.tracking_number,
          "tracking": [{
              "status": delivery.tracking["status"],
              "date": delivery.tracking["date"]
          }]
        }

        return data 

    def create_delivery(self, data):

        # Crea una instancia delivery desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
        
        data["status"] = "dispatched"
        data["tracking"] = {
            "status": "READY_FOR_PICK_UP",
            "date": format_date(get_current_datetime())
        }
        delivery = Delivery.from_dict(data)
        delivery = self.deliveries_repository.create_delivery(delivery)

        return delivery

    def update_delivery(self, delivery_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        delivery = self.get_delivery(delivery_id)

        if delivery:

            delivery = self.deliveries_repository.update_delivery(delivery_id, data)

            return delivery

        else:
            raise ValueError(f"Delivery of ID {delivery_id} doesn't exist.")

    def delete_delivery(self, delivery_id):

        # Realiza un hard-delete del delivery con la ID especificada, si es que existe.

        delivery = self.get_delivery(delivery_id)
        
        if delivery:

            delivery = self.deliveries_repository.hard_delete_delivery(delivery_id)

        else:
            raise ValueError(f"Delivery of ID {delivery_id} doesn't exist or is already deleted.")
          