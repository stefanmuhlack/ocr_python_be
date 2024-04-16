from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI()

# Define security and password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy database of users
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['hashed_password']):
        return False
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}

# Dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = authenticate_user(fake_users_db, token, "dummy")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    return user
# OCR Request Model
class OCRRequest(BaseModel):
    template_name: str
    rectangles: list

# Include routers
app.include_router(PDFService.router, prefix="/pdf", tags=["pdf"])
app.include_router(OCRService.router, prefix="/template", tags=["template"])

# Separate OCR and PDF handling in respective services for better modularity
