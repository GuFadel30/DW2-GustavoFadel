from database import SessionLocal, engine
from models import Book, Base
from sqlalchemy.sql import select

def seed_database():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar se já existem livros
        if db.query(Book).first():
            print("Database already seeded!")
            return

        # Lista de livros para seed
        books = [
            {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "ano": 1899,
                "genero": "Romance",
                "isbn": "9788535910682",
                "status": "Disponível"
            },
            {
                "titulo": "O Pequeno Príncipe",
                "autor": "Antoine de Saint-Exupéry",
                "ano": 1943,
                "genero": "Ficção",
                "isbn": "9788574123745",
                "status": "Disponível"
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "ano": 1949,
                "genero": "Ficção",
                "isbn": "9780451524935",
                "status": "Disponível"
            },
            {
                "titulo": "Memórias Póstumas de Brás Cubas",
                "autor": "Machado de Assis",
                "ano": 1881,
                "genero": "Romance",
                "isbn": "9788535910675",
                "status": "Disponível"
            },
            {
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "ano": 1954,
                "genero": "Aventura",
                "isbn": "9788533613379",
                "status": "Disponível"
            },
            {
                "titulo": "O Alquimista",
                "autor": "Paulo Coelho",
                "ano": 1988,
                "genero": "Drama",
                "isbn": "9780062315007",
                "status": "Disponível"
            },
            {
                "titulo": "Cem Anos de Solidão",
                "autor": "Gabriel García Márquez",
                "ano": 1967,
                "genero": "Drama",
                "isbn": "9788535914849",
                "status": "Disponível"
            },
            {
                "titulo": "O Corvo",
                "autor": "Edgar Allan Poe",
                "ano": 1845,
                "genero": "Terror",
                "isbn": "9788532529183",
                "status": "Disponível"
            },
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "autor": "J.K. Rowling",
                "ano": 1997,
                "genero": "Aventura",
                "isbn": "9788532530783",
                "status": "Disponível"
            },
            {
                "titulo": "O Nome do Vento",
                "autor": "Patrick Rothfuss",
                "ano": 2007,
                "genero": "Aventura",
                "isbn": "9788599296363",
                "status": "Disponível"
            },
            {
                "titulo": "O Iluminado",
                "autor": "Stephen King",
                "ano": 1977,
                "genero": "Terror",
                "isbn": "9788581050485",
                "status": "Disponível"
            },
            {
                "titulo": "A Metamorfose",
                "autor": "Franz Kafka",
                "ano": 1915,
                "genero": "Ficção",
                "isbn": "9788535914833",
                "status": "Disponível"
            },
            {
                "titulo": "O Hobbit",
                "autor": "J.R.R. Tolkien",
                "ano": 1937,
                "genero": "Aventura",
                "isbn": "9788535915563",
                "status": "Disponível"
            },
            {
                "titulo": "A Revolução dos Bichos",
                "autor": "George Orwell",
                "ano": 1945,
                "genero": "Ficção",
                "isbn": "9788535909555",
                "status": "Disponível"
            },
            {
                "titulo": "Drácula",
                "autor": "Bram Stoker",
                "ano": 1897,
                "genero": "Terror",
                "isbn": "9788525406279",
                "status": "Disponível"
            }
        ]
        
        for book_data in books:
            book = Book(**book_data)
            db.add(book)
        
        db.commit()
        print("Database seeded successfully!")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
