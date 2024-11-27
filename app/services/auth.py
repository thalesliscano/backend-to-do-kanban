import jwt
from datetime import datetime, timedelta, timezone

class AuthService:
    SECRET_KEY = "sua_chave_secreta_aqui"  # Substitua por uma chave secreta segura

    @staticmethod
    def gerar_token(user_id):
        """
        Gera um token JWT com base no user_id.
        """
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=2),  # Expira em 2 horas
                "iat": datetime.now(timezone.utc)  # Emitido em
            }
            token = jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")
            return token
        except Exception as e:
            print(f"Erro ao gerar token: {e}")
            return None

    @staticmethod
    def validar_token(token):
        """
        Valida um token JWT e retorna o user_id se o token for válido.
        """
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=["HS256"])
            return payload.get("user_id")  # Retorna o ID do usuário contido no token
        except jwt.ExpiredSignatureError:
            print("Token expirado.")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido.")
            return None
    