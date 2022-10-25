from fastapi import APIRouter, Request, Depends, status, Response, HTTPException
from fastapi.templating import Jinja2Templates
from libs.models import User
from libs.hashing import Hasher
from sqlalchemy.orm import Session
from libs.database import get_db
from configparser import ConfigParser
from jose import jwt

config = ConfigParser()
config.read("config/config.ini")


router = APIRouter()
templates = Jinja2Templates(directory="templates")
hasher = Hasher()


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """
    login page
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", tags=['auth'])
async def login_user(response: Response, request:Request, db:Session=Depends(get_db)):
    """
    login user
    """
    credentials = await request.form()
    username = credentials.get('username')
    password = credentials.get('password')

    errors = []
    try:
        user = db.query(User).filter(User.name==username).first()
        # print(username, password)
        # print(user.name, user.password)
        if user is None:
            errors.append(f"No user named {username}")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
        if hasher.verify_password(password, user.password):
            data = {"sub": username}
            jwt_token = jwt.encode(
                data, config.get("security", "jwt_secret_key"), algorithm=config.get("security", "algorithm")) # expires variable
            msg = "Login successfully."
            print(msg)
            response = templates.TemplateResponse("userinfo.html", {"request": request, "msg": msg})
            response.set_cookie(
                key="access_token", value=f"Bearer {jwt_token}", httponly=True)
            return response
        else: 
            print("Invalid username or password")
            errors.append("Invalid username or password")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
    
    except Exception as e:
        errors.append("Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="Invalid credentials")

