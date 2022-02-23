# Flask
from flask import Blueprint, request
# Utils
from src.utils.utils import is_seller
from src.utils.utils import authentication_required
# Validations
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.products.http.validation import product_validatable_fields

# Endpoints para CRUD de libros.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "product_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_products_blueprint(manage_products_usecase):
  
    from src.main import manage_orders_usecase

    products = Blueprint("products", __name__)

    @products.route("/products", methods = ["GET"])
    def get_products():

        products = manage_products_usecase.get_products()

        products_dict = []
        for product in products:
            products_dict.append(product.serialize())

        data = products_dict
        code = SUCCESS_CODE
        message = "Products obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code
      

    @products.route("/products/<string:product_id>", methods = ["GET"])
    def get_product(product_id):

        product = manage_products_usecase.get_product(product_id)

        if product:
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Products obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Products of ID {product_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code
      

    @products.route("/products", methods = ["POST"])
    @validate_schema_flask(product_validatable_fields.PRODUCT_CREATION_VALIDATABLE_FIELDS)
    # @authentication_required
    # @is_seller
    def create_product():

        body = request.get_json()

        try:
            product = manage_products_usecase.create_product(body)
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Product created succesfully"
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
      

    @products.route("/products/<string:product_id>", methods = ["PUT"])
    @validate_schema_flask(product_validatable_fields.PRODUCT_UPDATE_VALIDATABLE_FIELDS)
    # @authentication_required
    # @is_seller
    def update_product(product_id):

        body = request.get_json()

        try:
            product = manage_products_usecase.update_product(product_id, body)
            data = product.serialize()
            message = "Product updated succesfully"
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
      

    @products.route("/products/<string:product_id>", methods = ["DELETE"])
    @authentication_required
    @is_seller
    def delete_product(product_id):

        try:
            manage_products_usecase.delete_product(product_id)
            code = SUCCESS_CODE
            message = f"Product of ID {product_id} deleted succesfully."
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
      
      
    return products
