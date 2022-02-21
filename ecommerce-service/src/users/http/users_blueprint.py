# Flask
from flask import Blueprint, request
# Utils
from src.utils.utils import authentication_required, is_superuser
# Validations
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.users.http.validation import user_validatable_fields
# Password Hash Generator
from werkzeug.security import generate_password_hash


# Endpoints para CRUD de usuarios.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "user_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_users_blueprint(manage_users_usecase):

    users = Blueprint("users", __name__)
    
    @users.route("/users")
    def get_users():
      
      users = manage_users_usecase.get_users()
      
      users_dict = []
      for user in users:
          users_dict.append(user.serialize())

      data = users_dict
      code = SUCCESS_CODE
      message = "Users obtained succesfully"
      http_code = 200

      response = {
          "code": code,
          "message": message,
          "data": data,
      }
      
      return response, http_code

    @users.route("/create-superuser", methods = ["POST"])
    @validate_schema_flask(user_validatable_fields.SUPERUSER_CREATION_VALIDATABLE_FIELDS)
    def create_superuser():

        body = request.get_json()
        
        body["is_superuser"] = True
        
        password_hash = generate_password_hash(body["password"], method='sha256')
        
        body["password"] = password_hash

        try:
            superuser = manage_users_usecase.create_superuser(body)
            data = superuser.serialize()
            code = SUCCESS_CODE
            message = "Superuser created succesfully"
            http_code = 201

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code
      
    
    @users.route("/create-seller", methods = ["POST"])
    @validate_schema_flask(user_validatable_fields.SELLER_USER_CREATION_VALIDATABLE_FIELDS)
    @authentication_required
    @is_superuser
    def create_seller_user():

        body = request.get_json()
        
        body["is_seller"] = True
        
        password_hash = generate_password_hash(body["password"], method='sha256')
        
        body["password"] = password_hash

        try:
            user = manage_users_usecase.create_seller_user(body)
            data = user.serialize()
            code = SUCCESS_CODE
            message = "User Seller created succesfully"
            http_code = 201

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code
      
    
    @users.route("/create-user", methods = ["POST"])
    @validate_schema_flask(user_validatable_fields.MARKETPLACE_USER_CREATION_VALIDATABLE_FIELDS)
    @authentication_required
    @is_superuser
    def create_marketplace_user():
      
        body = request.get_json()
        
        password_hash = generate_password_hash(body["password"], method='sha256')
        
        body["password"] = password_hash

        try:
            user = manage_users_usecase.create_marketplace_user(body)
            data = user.serialize()
            code = SUCCESS_CODE
            message = "User created succesfully"
            http_code = 201

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code
      
      
    @users.route("/users/<string:user_id>", methods = ["DELETE"])
    @authentication_required
    @is_superuser
    def delete_user(user_id):

        try:
            manage_users_usecase.delete_user(user_id)
            code = SUCCESS_CODE
            message = f"User of ID {user_id} deleted succesfully."
            http_code = 200

        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code
      
      
    @users.route("/login", methods = ["POST"])
    def login_user():
      
        data = request.get_json()
        token = manage_users_usecase.get_token(data)
        
        return token
      
      
    return users
