from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional

# Authentication handler using OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Dummy user database
dummy_users_db = {
    'admin': {
        'username': 'admin',
        'hashed_password': pwd_context.hash('secret'),
        'disabled': False
    }
}

def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = dummy_users_db.get(username)
    if not user or not pwd_context.verify(password, user['hashed_password']):
        return None
    return user

# Dependency for route operations
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Assuming the token is the username for simplicity
    user = dummy_users_db.get(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    return user