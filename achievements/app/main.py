from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, users, achievements, comments, reactions, pages
from app.db.database import create_db_and_tables
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")


# routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(achievements.router)
app.include_router(comments.router)
app.include_router(reactions.router)
app.include_router(pages.router)
