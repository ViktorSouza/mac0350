from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, func

from app.core.security import get_current_user
from app.db.database import get_session
from app.models.models import Achievement, Reaction, ReactionType, User
from app.utils.templating import templates

router = APIRouter()


def build_reactions(session: Session, achievement_id: int, user_id: int):
    results = session.exec(
        select(Reaction.type, func.count())
        .where(Reaction.achievement_id == achievement_id)
        .group_by(Reaction.type)
    ).all()

    # normaliza chave para evitar inconsistência de tipo
    counts = {r_type.value: count for r_type, count in results}

    existing_reaction = session.exec(
        select(Reaction).where(
            Reaction.user_id == user_id,
            Reaction.achievement_id == achievement_id
        )
    ).first()

    user_reaction = existing_reaction.type if existing_reaction else None

    return [
        {
            "name": r_type.name,
            "value": r_type.value,
            "count": counts.get(r_type.value, 0),
            "selected": (
                user_reaction is not None and r_type == user_reaction
            )
        }
        for r_type in ReactionType
    ]


@router.get(
    "/achievement/{achievement_id}/reactions/select",
    response_class=HTMLResponse
)
async def get_reactions_from_achievement(
    achievement_id: int,
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    reactions = build_reactions(session, achievement_id, user.id)

    selected = next(
    (r for r in reactions if r["selected"]),
    reactions[0] if reactions else None
)
    return templates.TemplateResponse(
        "partials/reactions_select.html",
        {
            "request": request,
            "reactions": reactions,
            "achievement_id": achievement_id,
            "selected_reaction":selected
        }
    )


@router.post(
    "/achievement/{achievement_id}/reactions",
    response_class=HTMLResponse
)
async def react_to_achievement(
    request: Request,
    achievement_id: int,
    reaction_type: ReactionType = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    achievement = session.get(Achievement, achievement_id)
    if not achievement:
        raise HTTPException(status_code=404)

    existing_reaction = session.exec(
        select(Reaction).where(
            Reaction.user_id == user.id,
            Reaction.achievement_id == achievement_id
        )
    ).first()

    if existing_reaction:
        existing_reaction.type = reaction_type
        session.add(existing_reaction)
    else:
        session.add(
            Reaction(
                user_id=user.id,
                achievement_id=achievement_id,
                type=reaction_type
            )
        )

    session.commit()

    reactions = build_reactions(session, achievement_id, user.id)
    selected = next(
    (r for r in reactions if r["selected"]),
    reactions[0] if reactions else None
)
    return templates.TemplateResponse(
        "partials/reactions_select.html",
        {
            "request": request,
            "reactions": reactions,
            "achievement_id": achievement_id,
            "selected_reaction":selected
        }
    )