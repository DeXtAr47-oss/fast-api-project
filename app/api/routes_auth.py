from fastapi import APIRouter
from pydantic import BaseModel
from ..core.security import create_token

router = APIRouter()

class AuthInput(BaseModel):
    username: str
    password: str   

@router.post('/login')
def login(auth: AuthInput):
    if (auth.username == 'admin') and (auth.password == 'admin'):
        token = create_token({'sub': auth.username})
        return {'acess token': token}
    else:
        return {'error': 'invalid credentials'}
