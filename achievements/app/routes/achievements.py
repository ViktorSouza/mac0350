from fastapi import APIRouter, Form, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db.database import engine
from app.db.database import get_session
from app.models.models import Achievement,Reaction, ReactionType,Comment
from app.core.security import get_current_user
from app.utils.templating import templates
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.post("/achievements")
async def create_achievement(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    achievement = Achievement(
        title=title,
        description=description,
        user_id=user.id
    )
    session.add(achievement)
    session.commit()
    session.refresh(achievement)


    achievement = session.exec(
        select(Achievement)
        .options(joinedload(Achievement.user))
        .where(Achievement.id == achievement.id)
    ).first()

    return templates.TemplateResponse(
        "partials/achievement_card.html",
        {
            "request": request,
            "achievement": achievement,
            "reactions": ReactionType
        }
    )


@router.get("/achievements/{achievement_id}")
async def get_achievement_by_id(
    request: Request,
    achievement_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    achievement = session.exec(
        select(Achievement).where(Achievement.id == achievement_id)
    ).one()

    reactions = session.exec(
        select(Reaction).where(Reaction.achievement_id == achievement_id)
    ).all()

    comments = session.exec(
        select(Comment).where(Comment.achievement_id == achievement_id)
    ).all()

    return templates.TemplateResponse(
        "achievement.html",
        {"request": request, "achievement": achievement, "reactions":reactions
        ,"comments":comments
         }
    )
