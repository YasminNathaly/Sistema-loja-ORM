from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Categoria, Produto
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    produtos = db.query(Produto).all()
    return templates.TemplateResponse("index.html", {"request": request, "categorias": categorias, "produtos": produtos})
