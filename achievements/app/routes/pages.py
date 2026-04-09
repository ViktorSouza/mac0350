from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, desc
from sqlalchemy.orm import selectinload
from app.db.database import engine
from app.models.models import Achievement
from app.utils.templating import templates
from app.core.security import get_current_user_optional
from app.models.models import User

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request,user:User = Depends(get_current_user_optional) ):
    with Session(engine) as session:
        achievements = session.query(Achievement)\
        .options(selectinload(Achievement.user))\
        .order_by(desc(Achievement.created_at)).all()
    
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "achievements": achievements,"user":user}
    )

@router.get("/login")
async def login(request:Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@router.get("/create-user")
async def login(request:Request):
    return templates.TemplateResponse(
        "create-user.html",
        {"request": request}
    )
