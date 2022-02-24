# Flask
from flask import Blueprint, request
# Validations
from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from src.deliveries.http.validation import delivery_validatable_fields

# Endpoints para CRUD de Deliveries.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "delivery_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_deliveries_blueprint(manage_deliveries_usecase):
  
    # from src.main import manage_orders_usecase

    deliveries = Blueprint("deliveries", __name__)

    @deliveries.route("/deliveries", methods = ["GET"])
    def get_deliveries():

        deliveries = manage_deliveries_usecase.get_deliveries()

        deliveries_dict = []
        for delivery in deliveries:
            deliveries_dict.append(delivery.serialize())

        data = deliveries_dict
        code = SUCCESS_CODE
        message = "deliveries obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code
      

    @deliveries.route("/deliveries/<string:delivery_id>", methods = ["GET"])
    def get_delivery(delivery_id):

        delivery = manage_deliveries_usecase.get_delivery(delivery_id)

        if delivery:
            data = delivery.serialize()
            code = SUCCESS_CODE
            message = "deliveries obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"deliveries of ID {delivery_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code
      
      
    @deliveries.route("/deliveries/tracking/", methods = ["GET"])
    def get_delivery_tracking():
      
        body = request.get_json()
        tracking_number = body["tracking_number"]

        data = manage_deliveries_usecase.get_delivery_tracking(tracking_number)

        if data:
            code = SUCCESS_CODE
            message = "Delivery tracking obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"deliveries of ID {tracking_number} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code
      

    @deliveries.route("/deliveries", methods = ["POST"])
    def create_delivery():

        body = request.get_json()

        try:
            delivery = manage_deliveries_usecase.create_delivery(body)
            data = delivery.serialize()
            code = SUCCESS_CODE
            message = "delivery created succesfully"
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
      

    @deliveries.route("/deliveries/<string:delivery_id>", methods = ["PUT"])
    def update_delivery(delivery_id):

        body = request.get_json()

        try:
            delivery = manage_deliveries_usecase.update_delivery(delivery_id, body)
            data = delivery.serialize()
            message = "delivery updated succesfully"
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
      

    @deliveries.route("/deliveries/<string:delivery_id>", methods = ["DELETE"])
    def delete_delivery(delivery_id):

        try:
            manage_deliveries_usecase.delete_delivery(delivery_id)
            code = SUCCESS_CODE
            message = f"delivery of ID {delivery_id} deleted succesfully."
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
      
      
    return deliveries
