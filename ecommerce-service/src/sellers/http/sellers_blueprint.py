# Flask
from flask import Blueprint, request
# Utils
from src.utils.utils import is_superuser
from src.utils.utils import authentication_required
# Validations
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.sellers.http.validation import sellers_validatable_fields

# Endpoints para CRUD de EMPRESAS.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "seller_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_sellers_blueprint(manage_sellers_usecase):

    sellers = Blueprint("sellers", __name__)

    @sellers.route("/sellers", methods = ["GET"])
    @authentication_required
    @is_superuser
    def all_sellers():

        sellers = manage_sellers_usecase.get_sellers()

        sellers_dict = []
        for seller in sellers:
            sellers_dict.append(seller.serialize())

        data = sellers_dict
        code = SUCCESS_CODE
        message = "Sellers obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code
      

    @sellers.route("/sellers/<string:seller_id>", methods = ["GET"])
    @authentication_required
    @is_superuser
    def get_seller(seller_id):

        seller = manage_sellers_usecase.get_seller(seller_id)

        if seller:
            data = seller.serialize()
            code = SUCCESS_CODE
            message = "sellers obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Sellers of ID {seller_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code
      

    @sellers.route("/sellers", methods = ["POST"])
    @validate_schema_flask(sellers_validatable_fields.SELLER_CREATION_VALIDATABLE_FIELDS)
    @authentication_required
    @is_superuser
    def create_seller():

        body = request.get_json()

        try:
            seller = manage_sellers_usecase.create_seller(body)
            data = seller.serialize()
            code = SUCCESS_CODE
            message = "seller created succesfully"
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
      

    @sellers.route("/sellers/<string:seller_id>", methods = ["PUT"])
    @validate_schema_flask(sellers_validatable_fields.SELLER_UPDATE_VALIDATABLE_FIELDS)
    @authentication_required
    @is_superuser
    def update_seller(seller_id):

        body = request.get_json()

        try:
            seller = manage_sellers_usecase.update_seller(seller_id, body)
            data = seller.serialize()
            message = "seller updated succesfully"
            code = SUCCESS_CODE
            http_code = 200

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
      

    @sellers.route("/sellers/<string:seller_id>", methods = ["DELETE"])
    @authentication_required
    @is_superuser
    def delete_seller(seller_id):

        try:
            manage_sellers_usecase.delete_seller(seller_id)
            code = SUCCESS_CODE
            message = f"Seller of ID {seller_id} deleted succesfully."
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
      

    return sellers
