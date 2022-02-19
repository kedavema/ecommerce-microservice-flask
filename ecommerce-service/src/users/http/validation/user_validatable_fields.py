# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

SUPERUSER_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
    },

    "password": {
        "required": True,
        "type": "string",
    },

    "email": {
        "required": True,
        "type": "string",
    },

}


SELLER_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
    },

    "password": {
        "required": True,
        "type": "string",
    },

    "email": {
        "required": True,
        "type": "string",
    },
    "warehouse_address": {
        "required": True,
        "type": "string",
    },

}


USER_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
    },

    "password": {
        "required": True,
        "type": "string",
    },

    "email": {
        "required": True,
        "type": "string",
    },
    "shipping_address": {
        "required": True,
        "type": "string",
    },

}
