# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
# Entity
from src.orders.entities.order import Order
    
# Implementación con SQL Alchemy para el repositorio de Ordenes de compra.

class SQLAlchemyOrdersRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Order de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "orders"

        if test:
            table_name += "_test"

        self.orders_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("status", String(20)),
            Column("product_sku", Integer),
            Column("product_qty", Integer),
            Column("product_name", String(200)),
            Column("customer_id", Integer),
            Column("customer_address", String(200)),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Order, self.orders_table)

    def get_orders(self):
        
        with self.session_factory() as session:
            
            orders = session.query(Order).all()
            
            return orders

    def get_order(self, id):
        
        with self.session_factory() as session:

            order = session.query(Order).filter_by(id = id).first()
            
            return order

    def create_order(self, order):

        with self.session_factory() as session:

            session.add(order)
            session.commit()

            return order

    def change_order_status(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el ordero especificado.
        # Luego retorna el ordero con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Order).filter_by(id = id).update(fields)
            session.commit()
            order = session.query(Order).filter_by(id = id).first()
            
            return order

    def cancel_order(self, id):
      
        # Cancela(elimina) totalmente la orden de compra.

        with self.session_factory() as session:

            order = session.query(Order).get(id)
            session.delete(order)
            session.commit()
