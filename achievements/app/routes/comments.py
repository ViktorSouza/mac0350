from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.security import get_current_user
from app.db.database import get_session
from app.models.models import Comment, Achievement
from app.utils.templating import templates
from sqlmodel import select, Session

router = APIRouter()

@router.get("/achievements/{achievement_id}/comments", response_class=HTMLResponse)
async def get_comments(
    request: Request,
    achievement_id: int,
    session: Session = Depends(get_session)
):
    comments = session.exec(
        select(Comment).where(Comment.achievement_id == achievement_id)
    ).all()

    achievement = session.exec(select(Achievement).where(Achievement.id == achievement_id)).one()

    return templates.TemplateResponse(
        "partials/comment_list.html",
        {
            "request": request,
            "comments": comments,
            "achievement":achievement,
            "achievement_id": achievement_id
        }
    )


@router.post("/achievements/{achievement_id}/comments", response_class=HTMLResponse)
async def create_comment(
    request: Request,
    achievement_id: int,
    content: str = Form(...),
    user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    comment = Comment(
        user_id = user.id,
        achievement_id = achievement_id,
        content = content,
    )


    session.add(comment)
    session.commit()
    session.refresh(comment)

    comments = session.exec(
        select(Comment).where(Comment.achievement_id == achievement_id)
    ).all()

    achievement = session.exec(select(Achievement).where(Achievement.id == achievement_id)).one()

    return templates.TemplateResponse(
        "partials/comment_list.html",
        {
            "request": request,
            "comments": comments,
            "achievement":achievement,
            "achievement_id": achievement_id
        }
    )
