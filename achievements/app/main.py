# main.py

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables,engine
from models import Achievement
from datetime import datetime
from sqlmodel import Session
app = FastAPI() 

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# Mock database (MVP)
# =========================

#######
#
#
#
#
# COLOCAR REAÇÕES COMO CATAPIMBAS, ME IDENTIFICO, ETC
#
#
#
#
#
#######
ACHIEVEMENTS = [
    Achievement(
        id=1,
        user_id=1,
        title="First Login",
        description="User logged in for the first time",
        created_at=datetime.utcnow()
    ),
    Achievement(
        id=2,
        user_id=1,
        title="First Post",
        description="User created their first achievement",
        created_at=datetime.utcnow()
    ),
    Achievement(
        id=3,
        user_id=2,
        title="Explorer",
        description="Visited 10 different pages",
        created_at=datetime.utcnow()
    ),
]
COMMENTS = {}
REACTIONS = {}

def get_current_user():
    # TODO criar uma auth depois
    return {"id": 1, "username": "user1"}


# =========================
# Helpers
# =========================

def is_htmx(request: Request) -> bool:
    return "HX-Request" in request.headers


# =========================
# Base Pages
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
                context={"achievements": ACHIEVEMENTS}
    )


# =========================
# Feed (Timeline)
# =========================

@app.get("/feed", response_class=HTMLResponse)
async def get_feed(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partials/feed.html",
        context={"achievements": list(reversed(ACHIEVEMENTS))}
    )


# =========================
# Achievements (CRUD)
# =========================

@app.post("/achievements", response_class=HTMLResponse)
async def create_achievement(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    user=Depends(get_current_user)
):

    with Session(engine) as session:
            achievement = Achievement(
                title=title,
                description=description,
                user_id=user["id"]
            )
            session.add(achievement)
            session.commit()
            session.refresh(achievement)
            return templates.TemplateResponse(
                name = "partials/achievement_card.html",
                request = request,
                context={
                    "achievement": achievement
                }
            )



    return templates.TemplateResponse(
        request=request,
        name="partials/achievement_card.html",
        context={"achievement": achievement}
    )


@app.get("/achievements/{achievement_id}", response_class=HTMLResponse)
async def get_achievement(request: Request, achievement_id: int):
    achievement = next((a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)

    if not achievement:
        raise HTTPException(status_code=404)

    if not is_htmx(request):
        return templates.TemplateResponse(
            request=request,
            name="achievement.html",
            context={"achievement": achievement}
        )

    return templates.TemplateResponse(
        request=request,
        name="partials/achievement_card.html",
        context={"achievement": achievement}
    )


# =========================
# Reactions
# =========================

@app.post("/achievements/{achievement_id}/like", response_class=HTMLResponse)
async def like_achievement(
    request: Request,
    achievement_id: int,
    user=Depends(get_current_user)
):
    achievement = next((a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)

    if not achievement:
        raise HTTPException(status_code=404)

    achievement["likes"] += 1

    return templates.TemplateResponse(
        request=request,
        name="partials/achievement_card.html",
        context={"achievement": achievement}
    )


# =========================
# Comments
# =========================

@app.get("/achievements/{achievement_id}/comments", response_class=HTMLResponse)
async def get_comments(request: Request, achievement_id: int):
    comments = COMMENTS.get(achievement_id, [])

    return templates.TemplateResponse(
        request=request,
        name="partials/comment_list.html",
        context={
            "comments": comments,
            "achievement_id": achievement_id
        }
    )


@app.post("/achievements/{achievement_id}/comments", response_class=HTMLResponse)
async def create_comment(
    request: Request,
    achievement_id: int,
    content: str = Form(...),
    user=Depends(get_current_user)
):
    comment = {
        "user": user["username"],
        "content": content
    }

    COMMENTS.setdefault(achievement_id, []).append(comment)

    return templates.TemplateResponse(
        request=request,
        name="partials/comment_list.html",
        context={
            "comments": COMMENTS[achievement_id],
            "achievement_id": achievement_id
        }
    )


# =========================
# Profile
# =========================

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def profile(request: Request, user_id: int):
    user_achievements = [a for a in ACHIEVEMENTS if a["user_id"] == user_id]

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"achievements": user_achievements}
    )


# =========================
# Follow (placeholder)
# =========================

@app.post("/users/{user_id}/follow", response_class=HTMLResponse)
async def follow_user(request: Request, user_id: int):
    return HTMLResponse("<button>Following</button>")