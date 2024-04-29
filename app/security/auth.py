from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user or not user.check_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Could not validate credentials')
        user = {'username': username}
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate credentials')

