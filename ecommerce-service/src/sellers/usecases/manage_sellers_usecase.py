from src.sellers.entities.seller import Seller

# Casos de uso para el manejo de empresas.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageSellersUsecase:

    def __init__(self, sellers_repository):
        self.sellers_repository = sellers_repository

    def get_sellers(self):

        # Retorna una lista de entidades Seller desde el repositorio.

        return self.sellers_repository.get_sellers() 

    def get_seller(self, seller_id):

        # Retorna una instancia de Seller según la ID recibida.

        return self.sellers_repository.get_seller(seller_id)

    def create_seller(self, data):

        # Crea una instancia Seller desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        seller = Seller.from_dict(data)
        seller = self.sellers_repository.create_seller(seller)

        return seller

    def update_seller(self, seller_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        seller = self.get_seller(seller_id)

        if seller:

            seller = self.sellers_repository.update_seller(seller_id, data)

            return seller

        else:
            raise ValueError(f"Seller of ID {seller_id} doesn't exist.")

    def delete_seller(self, seller_id):

        # Realiza un hard-delete del sellero con la ID especificada, si es que existe.

        seller = self.get_seller(seller_id)
        
        if seller:

            seller = self.sellers_repository.delete_seller(seller_id)

        else:
            raise ValueError(f"seller of ID {seller_id} doesn't exist or is already deleted.")