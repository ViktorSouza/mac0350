# main.py

from fastapi import FastAPI, Request, Depends, HTTPException, Response, Cookie, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# "Banco de dados" em memória
users_db = []

# Modelo
class User(BaseModel):
    nome: str
    senha: str
    bio: str


# ---------------------------
# DEPENDÊNCIA (auth)
# ---------------------------
def get_current_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Não logado")

    user = next((u for u in users_db if u["nome"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    return user


# ---------------------------
# ROTAS
# ---------------------------

# Página inicial (criar usuário)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Criar usuário
@app.post("/users")
async def create_user(user: User):
    users_db.append(user.dict())
    return {"msg": "Usuário criado"}


# Página de login
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Fazer login
@app.post("/login")
def login(nome: str, senha: str, response: Response):
    user = next((u for u in users_db if u["nome"] == nome and u["senha"] == senha), None)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    response.set_cookie(key="session_user", value=nome)
    return {"msg": "Logado"}


# Página protegida
@app.get("/home", response_class=HTMLResponse)
def profile(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user
    })