from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey

from src.users.entities.user import User
    
# Implementación con SQL Alchemy para el repositorio de usuarios.

class SQLAlchemyUsersRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla User de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Users"

        if test:
            table_name += "_test"

        self.users_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("name", String(50)),
            Column("password", String(250)),
            Column("email", String(50)),
            Column("shipping_address", String(50)),
            Column("warehouse_address", String(50)),
            Column("is_superuser", Boolean()),
            Column("is_seller", Boolean()),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(User, self.users_table)


    def get_users(self):

        with self.session_factory() as session:
            
            users = session.query(User).all()
            return users
          
          
    def get_user(self, id):
        
        with self.session_factory() as session:

            user = session.query(User).filter_by(id = id).first()
            return user      
          
          
    def create_superuser(self, superuser):

        with self.session_factory() as session:

            session.add(superuser)
            session.commit()

            return superuser
          
          
    def create_seller_user(self, seller):

        with self.session_factory() as session:

            session.add(seller)
            session.commit()

            return seller
          
          
    def create_marketplace_user(self, user):

        with self.session_factory() as session:

            session.add(user)
            session.commit()

            return user
          
    
    def delete_user(self, id):

        with self.session_factory() as session:

            user = session.query(User).get(id)
            session.delete(user)
            session.commit()
          

    def get_user_by_email(self, email):
      
        with self.session_factory() as session:
          
            user = session.query(User).filter_by(email=email).first()
            return user
