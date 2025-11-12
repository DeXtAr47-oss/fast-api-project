from datetime import datetime, timezone, timedelta
from authlib.jose import jwt, JoseError
from .config import Settings

def create_token(data: dict, expire_min: int = 30):
    header = {'alg': Settings.JWT_ALGO}
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_min)
    payload = data.copy()
    payload.update({'exp': expire})
    return jwt.encode(header, payload, Settings.JWT_SECRET_KEY)

def verify_token(token: str):
    try:
        claims = jwt.decode(token, Settings.JWT_SECRET_KEY)
        claims.validate()
        return claims
    except JoseError:
        return None