from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.db.database import engine
from app.utils.templating import templates

router = APIRouter()

# mock (mesma ideia do original)


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def profile(request: Request, user_id: int):
    with Session(engine) as session:
        statement = select(Achievement).where(Achievement.user_id == user_id)
        user_achievements = session.exec(statement).all()

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "achievements": user_achievements
        }
    )


@router.post("/user/{user_id}/follow", response_class=HTMLResponse)
async def follow_user(request: Request, user_id: int):
    return HTMLResponse("<button>Following</button>")
