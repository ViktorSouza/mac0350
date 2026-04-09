from fastapi.templating import Jinja2Templates
import os

# Definimos o caminho absoluto para a pasta de templates
# Isso evita problemas dependendo de onde você inicia o uvicorn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory="./app/templates")
