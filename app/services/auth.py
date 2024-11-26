import jwt
import datetime
from flask import current_app

def gerar_token(usuario_id):
    """
    Gera um token JWT para o usuário
    """
    payload = {
        'id': usuario_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira em 1 hora
    }
    
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return token

