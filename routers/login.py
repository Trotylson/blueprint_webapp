from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from libs.database import get_db
from libs.models import User
from libs.hashing import Hasher
from jose import jwt
from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")
router = APIRouter()

@router.post("/login/token", tags = ['login'])
def retrieve_token_after_authentication(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    """
    OAuth2PasswordRequestForm schema
    """
    # print(form_data.username)
    # print(form_data.password)
    user = db.query(User).filter(User.name==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    if not Hasher.verify_password(form_data.password ,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    data = {"sub":form_data.username}
    jwt_token = jwt.encode(data, config.get("security", "jwt_secret_key"), config.get("security", "algorithm"))
    return {"access_token":jwt_token, "token_type": "bearer"}
