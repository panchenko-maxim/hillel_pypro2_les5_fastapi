import shutil
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session
from models import User
from database import get_db
from auth import get_current_user
from fastapi.responses import RedirectResponse
from pathlib import Path
from templates import templates
from schemas import UserSchemaOut


router = APIRouter()
AVATAR_DIR = 'static/avatars'

@router.get('/profile')
def profile(request: Request, user: UserSchemaOut = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login')
    return templates.TemplateRespons({'profile.html', {'request': request, 'user': user})

@router.post('/profile/avatar')
def upload_avatar(request: Request, db: Session = Depends(get_db), file: UploadFile = File(...), user: UserSchemaOut = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login')
    file_path = Path(AVATAR_DIR) / f'user_{user.id}.jpg'
    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_user = db.query(User).filter(User.id==user.id).first()
    db_user.avatar = f'{AVATAR_DIR}/user_{user.id}.jpg'
    db.commit()

    return RedirectResponse(url='/profile', status_code=303)