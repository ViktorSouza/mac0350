from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import User
from app.core.security import hash_password, create_access_token, verify_password

router = APIRouter()

@router.post("/user")
async def create_user(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    with Session(engine) as session:
        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        token = create_access_token({"sub": user.id})

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/"
    response.set_cookie("access_token", token, httponly=True)

    return response


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/"
    response.set_cookie(
        "access_token",
        token,
        httponly=True
    )

    return response

@router.post("/logout")
async def logout():
    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/"
    response.delete_cookie("access_token")
    return response