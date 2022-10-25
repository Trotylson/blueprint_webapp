from re import template
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import user, login, auth, common
from libs.database import ENGINE
from libs.models import Base


Base.metadata.create_all(bind=ENGINE)

app = FastAPI(title="eRR0r_!", version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(common.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(auth.router)
    