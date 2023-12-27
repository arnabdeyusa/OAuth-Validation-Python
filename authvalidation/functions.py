from flask import request,jsonify, _request_ctx_stack
from six.moves.urllib.request import urlopen
from functools import wraps
import os
import json
from jose import jwt

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Get bearer token from header
def get_token_auth_header(): 
    token = request.headers.get("Authorization", None)
    if not token:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = token.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)

    token = parts[1]
    return token

# Auth Decorator
def requires_auth(f):    
    @wraps(f)
    def decorated(*args, **kwargs):
        issuerEnv = os.getenv('ISSUER')
        audienceEnv = os.getenv('AUDIENCE')
        algoEnv = os.getenv('ALGO')
        authUrl = os.getenv('AUTHURL')
        token = get_token_auth_header()
        jsonurl = urlopen(authUrl)
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except Exception as err:
            return jsonify({'message' : f'{err}'}), 401
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload =  jwt.decode(
                                token,
                                rsa_key,
                                algorithms=[algoEnv],
                                audience=audienceEnv,
                                issuer=issuerEnv)
                
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated