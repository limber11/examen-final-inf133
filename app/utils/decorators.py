import json  # Importación del módulo json para trabajar con datos en formato JSON
from functools import wraps  # Importación de wraps para mantener la información del decorador original

from flask import jsonify  # Importación de jsonify para crear respuestas JSON
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request  # Importación de funciones para trabajar con JWT

# Decorador personalizado para requerir un JWT válido
def jwt_required(fn):
    @wraps(fn)  # Mantiene la información del decorador original
    def wrapper(*args, **kwargs):
        try:
            # Verifica que la solicitud tenga un JWT válido
            verify_jwt_in_request()
            # Llama a la función original si el JWT es válido
            return fn(*args, **kwargs)
        except Exception as e:
            # Devuelve un mensaje de error si el JWT no es válido
            return jsonify({"error": str(e)}), 401

    return wrapper

# Decorador personalizado para requerir roles específicos
def roles_required(roles=[]):
    def decorator(fn):
        @wraps(fn)  # Mantiene la información del decorador original
        def wrapper(*args, **kwargs):
            try:
                # Verifica que la solicitud tenga un JWT válido
                verify_jwt_in_request()
                # Obtiene la identidad del usuario actual desde el JWT
                current_user = get_jwt_identity()
                # Obtiene los roles del usuario actual
                user_roles = json.loads(current_user.get("roles", []))
                # Verifica si el usuario tiene al menos uno de los roles requeridos
                if not set(roles).intersection(user_roles):
                    # Devuelve un mensaje de error si el usuario no tiene los roles requeridos
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403
                # Llama a la función original si el usuario tiene los roles requeridos
                return fn(*args, **kwargs)
            except Exception as e:
                # Devuelve un mensaje de error si hay algún problema con el JWT
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator
