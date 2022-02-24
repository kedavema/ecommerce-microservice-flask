# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un producto. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

SELLER_CREATION_VALIDATABLE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
    },

    "short_desc": {
        "required": True,
        "type": "string",
    },

    "warehouse": {
        "required": True,
        "type": "string",
    },

}

SELLER_UPDATE_VALIDATABLE_FIELDS = {

    "name": {
        "required": False,
        "type": "string",
    },

    "short_desc": {
        "required": False,
        "type": "string",
    },

    "warehouse": {
        "required": False,
        "type": "string",
    },

}
