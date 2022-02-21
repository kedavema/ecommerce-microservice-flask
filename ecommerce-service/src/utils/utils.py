import jwt
from src import main
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timezone

# Funciones de utilidad para el sistema completo.

# Si bien no va dentro de ninguna de las carpetas de contexto,
# estas funciones corresponden a la capa más interna de Clean Architecture, que corresponde
# a la capa Entities. Esta capa no solamente puede contener entidades, sino cualquier código
# que es usado a nivel de aplicación completo.

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def filter_dict(dict, fields):

    # Filtra el diccionario entrante, retornando nuevo diccionario
    # sólo con los campos definidos y descartando los demás.

    filtered_dict = {}

    for key in dict:

        if key in fields:
            filtered_dict[key] = dict[key]

    return filtered_dict

def format_date(datetime):

    # Retorna una representación en String de una fecha/hora dada.

    return datetime.strftime(DATE_FORMAT)

def get_current_datetime():

    # Retorna la fecha actual en UTC-0
    
    return datetime.now(timezone.utc)
  

def authentication_required(f):
  
    # Decorador encargado de verificar si el usuario está autenticado.
  
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        
        if "auth-token" in request.headers:
            token = request.headers["auth-token"]
            
        if not token:
            return jsonify({"message": "an auth token is missing"}), 401
          
        try:
            data = jwt.decode(token, "LKAjsuhifiopaosuNAKSJXNC98lak)09a23")
            kwargs["id"] = data["id"] 
            
        except:
            return jsonify({"message": "invalid auth token"})
          
        return f(*args, **kwargs)
      
    return decorator
  
  
def is_seller(f):
  
    # Decorador encargado de verificar si es un vendedor.
    
    @wraps(f)
    def decorator(*args, **kwargs):
      
        user_id = kwargs.pop("id")
        
        user = main.manage_users_usecase.get_user(user_id)
        
        if not user.is_seller:
          
            return jsonify({"message": "User is not authorized"})
          
        return f(*args, **kwargs)
      
    return decorator
  
  
def is_superuser(f):
  
    # Decorador encargado de verificar si es un superusuario.
    
    @wraps(f)
    def decorator(*args, **kwargs):
      
        user_id = kwargs.pop("id")
        
        user = main.manage_users_usecase.get_user(user_id)
        
        if user is None:
          
            return jsonify({"message": "You must create a superuser first"})
        
        elif not user.is_superuser:
          
            return jsonify({"message": "User is not authorized"})
          
        return f(*args, **kwargs)
      
    return decorator
  