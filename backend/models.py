from sqlalchemy import Column, Integer, String, Date
from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime
from database import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, unique=True)
    autor = Column(String, index=True)
    ano = Column(Integer)
    genero = Column(String)
    isbn = Column(String, unique=True, nullable=True)
    status = Column(String, default="Disponível")
    data_emprestimo = Column(Date, nullable=True)

class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano: int
    genero: str
    isbn: Optional[str] = None
    status: str = "Disponível"

    @validator('ano')
    def validar_ano(cls, v):
        ano_atual = datetime.now().year
        if v < 1900 or v > ano_atual:
            raise ValueError(f'Ano deve estar entre 1900 e {ano_atual}')
        return v

    @validator('status')
    def validar_status(cls, v):
        status_validos = ["Disponível", "Emprestado", "Em Manutenção"]
        if v not in status_validos:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(status_validos)}')
        return v

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    genero: Optional[str] = None
    status: Optional[str] = None
    isbn: Optional[str] = None

    @validator('ano')
    def validar_ano(cls, v):
        if v is not None:
            ano_atual = datetime.now().year
            if v < 1900 or v > ano_atual:
                raise ValueError(f'Ano deve estar entre 1900 e {ano_atual}')
        return v

    @validator('status')
    def validar_status(cls, v):
        if v is not None:
            status_validos = ["Disponível", "Emprestado", "Em Manutenção"]
            if v not in status_validos:
                raise ValueError(f'Status deve ser um dos seguintes: {", ".join(status_validos)}')
        return v

class Livro(LivroBase):
    id: int
    data_emprestimo: Optional[date] = None

    class Config:
        orm_mode = True
