# Flask
from flask import Blueprint, request
# Utils
from src.utils.utils import is_seller
from src.utils.utils import authentication_required
# validation
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.orders.http.validation import order_validatable_fields


# Endpoints para CRUD de Ordenes de compra.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "order_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_orders_blueprint(manage_orders_usecase):
  
    from src.main import manage_products_usecase

    orders = Blueprint("orders", __name__)

    @orders.route("/orders", methods = ["GET"])
    @authentication_required
    @is_seller
    def get_orders():

        orders = manage_orders_usecase.get_orders()

        orders_dict = []
        for order in orders:
            orders_dict.append(order.serialize())

        data = orders_dict
        code = SUCCESS_CODE
        message = "orders obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code

    @orders.route("/orders/<string:order_id>", methods = ["GET"])
    @authentication_required
    @is_seller
    def get_order(order_id):

        order = manage_orders_usecase.get_order(order_id)

        if order:
            data = order.serialize()
            code = SUCCESS_CODE
            message = "Orders obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Orders of ID {order_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code

    @orders.route("/orders", methods = ["POST"])
    @validate_schema_flask(order_validatable_fields.ORDER_CREATION_VALIDATABLE_FIELDS)
    def create_order():
      
        body = request.get_json()
        body["status"] = "created"
        
        product = manage_products_usecase.get_product(body["product_sku"])
        body["product_name"] = product.name
        
        try:
            order = manage_orders_usecase.create_order(body)
            data = order.serialize()
            code = SUCCESS_CODE
            message = "order created succesfully"
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
      

    @orders.route("/orders/<string:order_id>", methods = ["PATCH"])
    @validate_schema_flask(order_validatable_fields.CHANGE_ORDER_STATUS_VALIDATABLE_FIELDS)
    @authentication_required
    @is_seller
    def change_order_status(order_id):

        body = request.get_json()
        status = body["status"]
        
        try:
            order = manage_orders_usecase.change_order_status(order_id, body, manage_products_usecase)
            data = order.serialize()
            message = f"Order status changed to {status}"
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
      

    @orders.route("/orders/<string:order_id>", methods = ["DELETE"])
    def cancel_order(order_id):

        try:
            manage_orders_usecase.cancel_order(order_id, manage_products_usecase)
            code = SUCCESS_CODE
            message = f"Order of ID {order_id} cancelled succesfully."
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


    return orders
