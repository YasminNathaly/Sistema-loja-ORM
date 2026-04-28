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
@app.post("/add_categoria")
def add_categoria(request: Request, nome: str = Form(...), db: Session = Depends(get_db)):
    categoria = Categoria(nome=nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return RedirectResponse(url="/", status_code=303)
@app.post("/add_produto")
def add_produto(request: Request, nome: str = Form(...), categoria_id: int = Form(...), db: Session = Depends(get_db)):
    produto = Produto(nome=nome, categoria_id=categoria_id)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return RedirectResponse(url="/", status_code=303)
@app.post("/delete_categoria/{categoria_id}") 
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
@app.post("/delete_produto/{produto_id}")
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
