# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, JSON
# Entity
from src.deliveries.entities.delivery import Delivery
    
# Implementación con SQL Alchemy para el repositorio de deliveries.

class SQLAlchemyDeliveriesRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla delivery de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "deliveries"

        if test:
            table_name += "_test"

        self.deliveries_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("tracking_number", Integer, primary_key = True, nullable=True),
            Column("order", JSON, nullable=True),
            Column("origin", JSON, nullable=True),
            Column("destination", JSON, nullable=True),
            Column("status", String(200), nullable=True),
            Column("tracking", JSON, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Delivery, self.deliveries_table)
        

    def get_deliveries(self):
        
        with self.session_factory() as session:
            
            deliveries = session.query(Delivery).all()
            return deliveries
          

    def get_delivery(self, id):
        
        with self.session_factory() as session:

            delivery = session.query(Delivery).filter_by(tracking_number = id).first()
            return delivery
          
          
    def get_delivery_tracking(self, tracking_number):
        
        with self.session_factory() as session:

            delivery = session.query(Delivery).filter_by(tracking_number=tracking_number).first()
            
            return delivery
          

    def create_delivery(self, delivery):
      
        with self.session_factory() as session:

            session.add(delivery)
            session.commit()

            return delivery
          

    def update_delivery(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el deliveryo especificado.
        # Luego retorna el delivery con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Delivery).filter_by(id = id).update(fields)
            session.commit()
            
            delivery = session.query(Delivery).filter_by(id = id).first()
            return delivery
          

    def hard_delete_delivery(self, id):

        with self.session_factory() as session:

            delivery = session.query(Delivery).get(id)
            session.delete(delivery)
            session.commit()
