# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar una orden de compra. 
# Estos esquemas son usados en el decorador "validate_schema_flask" 
# usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

ORDER_CREATION_VALIDATABLE_FIELDS = {

    "product_sku": {
        "required": True,
        "type": "integer",
    },

    "product_qty": {
        "required": True,
        "type": "integer",
    },

}

CHANGE_ORDER_STATUS_VALIDATABLE_FIELDS = {

    "status": {
        "required": True,
        "type": "string",
    },

}
