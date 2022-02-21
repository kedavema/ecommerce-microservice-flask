# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
# Entity
from src.sellers.entities.seller import Seller
    
# Implementación con SQL Alchemy para el repositorio de sellers.

class SQLAlchemySellersRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla seller de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "sellers"

        if test:
            table_name += "_test"

        self.sellers_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("name", String(50)),
            Column("short_desc", String(100)),
            Column("warehouse", String(200)),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Seller, self.sellers_table)

    def get_sellers(self):
        
        with self.session_factory() as session:
            
            sellers = session.query(Seller).all()
            return sellers

    def get_seller(self, id):
        
        with self.session_factory() as session:

            seller = session.query(Seller).filter_by(id = id).first()
            return seller

    def create_seller(self, seller):

        with self.session_factory() as session:

            session.add(seller)
            session.commit()

            return seller

    def update_seller(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el seller especificado.
        # Luego retorna el seller con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Seller).filter_by(id = id).update(fields)
            session.commit()
            
            seller = session.query(Seller).filter_by(id = id).first()
            
            return seller

    def delete_seller(self, id):

        with self.session_factory() as session:

            seller = session.query(Seller).get(id)
            session.delete(seller)
            session.commit()
