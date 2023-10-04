import jwt
from django.http import JsonResponse
from rest_framework.response import Response


def get_username_from_token(request):
    token = request.META.get("HTTP_AUTHORIZATION", "").split("Bearer ")[-1]
    try:
        decoded_token = jwt.decode(token, "secret_key", algorithms=["HS256"])
        username = decoded_token.get("sub")
        token_type = decoded_token.get("type")
        if token_type == "access":
            return {"username": username}
        else:
            return JsonResponse("Token is not access")
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.DecodeError:
        return {"error": "Decode Error"}
