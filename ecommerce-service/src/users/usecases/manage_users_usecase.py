import jwt

import datetime

from flask import make_response, jsonify

from src.users.entities.user import User

from werkzeug.security import check_password_hash

# Casos de uso para el manejo de usuarios.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageUsersUsecase:

    def __init__(self, users_repository):
        self.users_repository = users_repository
        
        
    def get_users(self):

      # Retorna una lista de entidades User desde el repositorio.

      return self.users_repository.get_users()
    
    
    def get_user(self, user_id):

        # Retorna una instancia de User según la ID recibida.

        return self.users_repository.get_user(user_id)


    def create_superuser(self, data):

        # Crea una instancia User desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        user = User.from_dict(data)
        user = self.users_repository.create_superuser(user)

        return user
      
      
    def create_seller_user(self, data):

        # Crea una instancia User desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        user = User.from_dict(data)
        user = self.users_repository.create_seller_user(user)

        return user
      
      
    def create_marketplace_user(self, data):

        # Crea una instancia User desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        user = User.from_dict(data)
        user = self.users_repository.create_marketplace_user(user)

        return user
      
      
    def delete_user(self, user_id):

        # Realiza un hard-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        user = self.get_user(user_id)

        if user:
            user = self.users_repository.delete_user(user_id)

        else:
            raise ValueError(f"User of ID {user_id} doesn't exist or is already deleted.")
          
          
    def get_token(self, data):
      
        # Retorna un token de autenticacion para el usuario al hacer login
        
        if not data or not data["email"] or not data["password"]:
            make_response("Could not verify", 401, {"www.authentication": "Login required"})
        
        utcnow = datetime.datetime.utcnow()
        hour = datetime.timedelta(minutes=60)
        SECRET_KEY = "LKAjsuhifiopaosuNAKSJXNC98lak)09a23"
        
        user = self.users_repository.get_user_by_email(data["email"])
        
        if user is None:
          
            return jsonify({"message": "You must create a user first"})
        
        elif check_password_hash(user.password, data["password"]):
          
            token = jwt.encode({"id": user.id, "exp": utcnow + hour}, SECRET_KEY)

            return jsonify({"token": token.decode('UTF-8')})
          
          
          
          
          
          
