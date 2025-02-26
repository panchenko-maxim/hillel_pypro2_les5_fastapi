from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session
from models import User
from database import get_db
from auth import get_current_user
from fastapi.responses import RedirectResponse
from pathlib import Path
from templates import template
from schemas import UserSchemaOut

router = APIRouter()

@router.get('/profile')
def profile(request: Request, db: Session = Depends(get_db), user: UserSchemaOut = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login')