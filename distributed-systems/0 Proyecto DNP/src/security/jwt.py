import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

SECRET = "supersecret"

def create_token(data: dict):
    return jwt.encode(data, SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class JWTBearer(HTTPBearer):
    def __call__(self, request):
        token = super().__call__(request)
        return verify_token(token.credentials)