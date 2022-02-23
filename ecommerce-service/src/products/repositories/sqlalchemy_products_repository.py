# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey
# Entity
from src.products.entities.product import Product
    
# Implementación con SQL Alchemy para el repositorio de Productos.

class SQLAlchemyProductsRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Product de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Products"

        if test:
            table_name += "_test"

        self.products_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("name", String(50)),
            Column("short_desc", String(100)),
            Column("qty", Integer),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Product, self.products_table)
        

    def get_products(self):
        
        with self.session_factory() as session:
            
            products = session.query(Product).all()
            return products
          

    def get_product(self, id):
        
        with self.session_factory() as session:

            product = session.query(Product).filter_by(id = id).first()
            return product
          

    def create_product(self, product):

        with self.session_factory() as session:

            session.add(product)
            session.commit()

            return product
          

    def update_product(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el producto especificado.
        # Luego retorna el producto con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Product).filter_by(id = id).update(fields)
            session.commit()
            
            product = session.query(Product).filter_by(id = id).first()
            return product
          

    def hard_delete_product(self, id):

        with self.session_factory() as session:

            product = session.query(Product).get(id)
            session.delete(product)
            session.commit()


    def decrease_qty(self, id, product_qty):
      
        with self.session_factory() as session:
          
            product = session.query(Product).get(id)
            product.qty -= product_qty
            session.commit()
            
            
    def increase_qty(self, id, product_qty):
      
        with self.session_factory() as session:
          
            product = session.query(Product).get(id)
            product.qty += product_qty
            session.commit()
            