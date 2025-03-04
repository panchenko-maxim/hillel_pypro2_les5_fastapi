from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth import router as auth_router
from profile import router as profile_router
import database

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth_router)
app.include_router(profile_router)

@app.on_event('startup')
def startup():
    database.init_db()