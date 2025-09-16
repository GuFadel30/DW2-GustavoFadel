from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, unique=True)
    autor = Column(String, index=True)
    ano = Column(Integer)
    genero = Column(String)
    isbn = Column(String, unique=True, nullable=True)
    status = Column(String)
    data_emprestimo = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
