from http.client import responses

from fastapi import  APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserSchemaIn, UserSchemaOut
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from templates.templates import templates

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'])

@router.get('/register')
def register_form(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.post('/register')
def register(request: Request, form_data: UserSchemaIn = Depends(UserSchemaIn.as_form), db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(form_data.password)
    user = User(username=form_data.username, password=hashed_pwd)
    db.add(user)
    db.commit()
    return RedirectResponse(url='/login', status_code=303)

@router.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.post('/login')
def login(
        request: Request,
        username = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password):
        response = RedirectResponse(url='/profile', status_code=303)
        response.set_cookie(key='user_id', value=user.id)
        return response
    return RedirectResponse(url='/login', status_code=303)

@router.get('/logout')
def logout():
    response = RedirectResponse(url='/')
    response.delete_cookie('user_id')
    return response

def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserSchemaOut|None:
    user_id = request.cookies.get('user_id')
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return UserSchemaOut.model_validate(user)
    return None



