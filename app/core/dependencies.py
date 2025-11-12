from fastapi import Header, HTTPException
from .config import Settings
from .security import verify_token

def get_api_key(api_key: str = Header(...)):
    if api_key != Settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid api key")

def get_current_user(token: str = Header(...)):
    paylaod = verify_token(token=token)
    if not paylaod:
        raise HTTPException(status_code=401, detail='Invalid JWT token')
    else:
        return paylaod
    


