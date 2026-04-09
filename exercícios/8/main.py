from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

likes = 0  # estado simples (em memória)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "pagina": "/aba/curtidas"}
    )


@app.get("/aba/curtidas", response_class=HTMLResponse)
async def curtidas(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "pagina": "/aba/curtidas"}
        )
    return templates.TemplateResponse(
        "curtidas.html",
        {"request": request, "likes": likes}
    )


@app.get("/aba/jupiter", response_class=HTMLResponse)
async def jupiter(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "pagina": "/aba/jupiter"}
        )
    return templates.TemplateResponse("jupiter.html", {"request": request})


@app.get("/aba/professor", response_class=HTMLResponse)
async def professor(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "pagina": "/aba/professor"}
        )
    return templates.TemplateResponse("professor.html", {"request": request})


@app.post("/curtir", response_class=HTMLResponse)
async def curtir(request: Request):
    global likes
    likes += 1
    return templates.TemplateResponse(
        "likes.html",
        {"request": request, "likes": likes}
    )


@app.post("/reset", response_class=HTMLResponse)
async def reset(request: Request):
    global likes
    likes = 0
    return templates.TemplateResponse(
        "likes.html",
        {"request": request, "likes": likes}
    )
