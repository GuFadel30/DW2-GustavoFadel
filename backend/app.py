from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date
import models
import database

# Criar o banco e as tabelas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Biblioteca Escolar")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/livros/", response_model=models.Livro, status_code=201)
def criar_livro(livro: models.LivroCreate, db: Session = Depends(get_db)):
    # Verificar se já existe livro com o mesmo título
    if db.query(models.Livro).filter(models.Livro.titulo == livro.titulo).first():
        raise HTTPException(status_code=400, detail="Já existe um livro com este título")
    
    # Verificar se já existe livro com o mesmo ISBN (se fornecido)
    if livro.isbn and db.query(models.Livro).filter(models.Livro.isbn == livro.isbn).first():
        raise HTTPException(status_code=400, detail="Já existe um livro com este ISBN")
    
    db_livro = models.Livro(**livro.dict())
    db.add(db_livro)
    
    try:
        db.commit()
        db.refresh(db_livro)
        return db_livro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar livro")

@app.get("/livros/", response_model=List[models.Livro])
def listar_livros(
    search: Optional[str] = None,
    genero: Optional[str] = None,
    ano: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Livro)
    
    if search:
        query = query.filter(
            or_(
                models.Livro.titulo.ilike(f"%{search}%"),
                models.Livro.autor.ilike(f"%{search}%")
            )
        )
    
    if genero:
        query = query.filter(models.Livro.genero == genero)
    
    if ano:
        query = query.filter(models.Livro.ano == ano)
    
    if status:
        query = query.filter(models.Livro.status == status)
    
    return query.all()

@app.get("/livros/{livro_id}", response_model=models.Livro)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@app.put("/livros/{livro_id}", response_model=models.Livro)
def atualizar_livro(livro_id: int, livro: models.LivroUpdate, db: Session = Depends(get_db)):
    db_livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Verificar título único se estiver sendo atualizado
    if livro.titulo and livro.titulo != db_livro.titulo:
        if db.query(models.Livro).filter(models.Livro.titulo == livro.titulo).first():
            raise HTTPException(status_code=400, detail="Já existe um livro com este título")
    
    # Verificar ISBN único se estiver sendo atualizado
    if livro.isbn and livro.isbn != db_livro.isbn:
        if db.query(models.Livro).filter(models.Livro.isbn == livro.isbn).first():
            raise HTTPException(status_code=400, detail="Já existe um livro com este ISBN")
    
    for key, value in livro.dict(exclude_unset=True).items():
        setattr(db_livro, key, value)
    
    try:
        db.commit()
        db.refresh(db_livro)
        return db_livro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar livro")

@app.delete("/livros/{livro_id}", status_code=204)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:
        db.delete(livro)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar livro")

@app.post("/livros/{livro_id}/emprestar", response_model=models.Livro)
def emprestar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.status != "Disponível":
        raise HTTPException(status_code=400, detail="Livro não está disponível para empréstimo")
    
    livro.status = "Emprestado"
    livro.data_emprestimo = date.today()
    
    try:
        db.commit()
        db.refresh(livro)
        return livro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao emprestar livro")

@app.post("/livros/{livro_id}/devolver", response_model=models.Livro)
def devolver_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.status != "Emprestado":
        raise HTTPException(status_code=400, detail="Livro não está emprestado")
    
    livro.status = "Disponível"
    livro.data_emprestimo = None
    
    try:
        db.commit()
        db.refresh(livro)
        return livro
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao devolver livro")
