import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


def get_username_from_token(request):
    token = request.META.get("HTTP_AUTHORIZATION", "").split("Bearer ")[-1]
    try:
        decoded_token = jwt.decode(token, "secret_key", algorithms=["HS256"])
        username = decoded_token.get("sub")
        token_type = decoded_token.get("type")
        if token_type == "access":
            return {"username": username}
        else:
            return {"error": "Token is not access"}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.DecodeError:
        return {"error": "Decode Error"}


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        data = get_username_from_token(request)

        if data is None:
            return None

        username = data.get("username")

        if "error" in data:
            raise AuthenticationFailed(data["error"])

        return (username, None)
