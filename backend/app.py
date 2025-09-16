from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import models
from database import engine, get_db

app = FastAPI(title="Biblioteca Escolar API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/livros")
async def get_livros(
    search: Optional[str] = None,
    genero: Optional[str] = None,
    ano: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)
    
    if search:
        query = query.filter(
            (models.Book.titulo.ilike(f"%{search}%")) |
            (models.Book.autor.ilike(f"%{search}%"))
        )
    
    if genero:
        query = query.filter(models.Book.genero == genero)
    
    if ano:
        query = query.filter(models.Book.ano == ano)
    
    if status:
        query = query.filter(models.Book.status == status)
    
    livros = query.all()
    return livros

@app.post("/livros")
async def create_livro(titulo: str, autor: str, ano: int, genero: str, 
                      isbn: Optional[str] = None, db: Session = Depends(get_db)):
    # Validar título único
    existing = db.query(models.Book).filter(models.Book.titulo == titulo).first()
    if existing:
        raise HTTPException(status_code=400, detail="Título já existe")
    
    # Validar ano
    current_year = datetime.now().year
    if ano < 1900 or ano > current_year:
        raise HTTPException(status_code=400, detail="Ano inválido")
    
    livro = models.Book(
        titulo=titulo,
        autor=autor,
        ano=ano,
        genero=genero,
        isbn=isbn,
        status="Disponível"
    )
    
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro

@app.put("/livros/{id}")
async def update_livro(id: int, titulo: str, autor: str, ano: int, genero: str,
                      isbn: Optional[str] = None, db: Session = Depends(get_db)):
    livro = db.query(models.Book).filter(models.Book.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Validar título único
    existing = db.query(models.Book).filter(
        models.Book.titulo == titulo,
        models.Book.id != id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Título já existe")
    
    livro.titulo = titulo
    livro.autor = autor
    livro.ano = ano
    livro.genero = genero
    livro.isbn = isbn
    
    db.commit()
    db.refresh(livro)
    return livro

@app.delete("/livros/{id}")
async def delete_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Book).filter(models.Book.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(livro)
    db.commit()
    return {"message": "Livro deletado com sucesso"}

@app.post("/livros/{id}/emprestar")
async def emprestar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Book).filter(models.Book.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.status != "Disponível":
        raise HTTPException(status_code=400, detail="Livro não está disponível")
    
    livro.status = "Emprestado"
    livro.data_emprestimo = datetime.now()
    
    db.commit()
    db.refresh(livro)
    return livro

@app.post("/livros/{id}/devolver")
async def devolver_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Book).filter(models.Book.id == id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.status != "Emprestado":
        raise HTTPException(status_code=400, detail="Livro não está emprestado")
    
    livro.status = "Disponível"
    livro.data_emprestimo = None
    
    db.commit()
    db.refresh(livro)
    return livro
