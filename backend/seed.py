from database import SessionLocal, engine
import models
from datetime import date

# Criar as tabelas
models.Base.metadata.create_all(bind=engine)

# Lista de livros para seed
livros = [
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
        "isbn": "9788574066943",
        "status": "Disponível"
    },
    {
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949,
        "genero": "Ficção",
        "isbn": "9788535914849",
        "status": "Disponível"
    },
    {
        "titulo": "Cem Anos de Solidão",
        "autor": "Gabriel García Márquez",
        "ano": 1967,
        "genero": "Drama",
        "isbn": "9788501009548",
        "status": "Disponível"
    },
    {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954,
        "genero": "Aventura",
        "isbn": "9788533613379",
        "status": "Emprestado"
    },
    {
        "titulo": "Crime e Castigo",
        "autor": "Fiódor Dostoiévski",
        "ano": 1866,
        "genero": "Drama",
        "isbn": "9788573261134",
        "status": "Disponível"
    },
    {
        "titulo": "O Alquimista",
        "autor": "Paulo Coelho",
        "ano": 1988,
        "genero": "Ficção",
        "isbn": "9788571640245",
        "status": "Em Manutenção"
    },
    {
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "ano": 1881,
        "genero": "Romance",
        "isbn": "9788535910693",
        "status": "Disponível"
    },
    {
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J.K. Rowling",
        "ano": 1997,
        "genero": "Aventura",
        "isbn": "9788532511010",
        "status": "Disponível"
    },
    {
        "titulo": "A Metamorfose",
        "autor": "Franz Kafka",
        "ano": 1915,
        "genero": "Terror",
        "isbn": "9788535902785",
        "status": "Disponível"
    },
    {
        "titulo": "O Hobbit",
        "autor": "J.R.R. Tolkien",
        "ano": 1937,
        "genero": "Aventura",
        "isbn": "9788595084742",
        "status": "Disponível"
    },
    {
        "titulo": "Orgulho e Preconceito",
        "autor": "Jane Austen",
        "ano": 1813,
        "genero": "Romance",
        "isbn": "9788544001820",
        "status": "Disponível"
    },
    {
        "titulo": "O Corvo",
        "autor": "Edgar Allan Poe",
        "ano": 1845,
        "genero": "Terror",
        "isbn": "9788594318237",
        "status": "Disponível"
    },
    {
        "titulo": "Frankenstein",
        "autor": "Mary Shelley",
        "ano": 1818,
        "genero": "Terror",
        "isbn": "9788594318244",
        "status": "Emprestado"
    },
    {
        "titulo": "O Morro dos Ventos Uivantes",
        "autor": "Emily Brontë",
        "ano": 1847,
        "genero": "Romance",
        "isbn": "9788594318251",
        "status": "Disponível"
    },
    {
        "titulo": "Alice no País das Maravilhas",
        "autor": "Lewis Carroll",
        "ano": 1865,
        "genero": "Ficção",
        "isbn": "9788594318268",
        "status": "Disponível"
    },
    {
        "titulo": "A Revolução dos Bichos",
        "autor": "George Orwell",
        "ano": 1945,
        "genero": "Ficção",
        "isbn": "9788594318275",
        "status": "Disponível"
    },
    {
        "titulo": "O Retrato de Dorian Gray",
        "autor": "Oscar Wilde",
        "ano": 1890,
        "genero": "Terror",
        "isbn": "9788594318282",
        "status": "Em Manutenção"
    },
    {
        "titulo": "A Odisseia",
        "autor": "Homero",
        "ano": 1900,
        "genero": "Aventura",
        "isbn": "9788594318299",
        "status": "Disponível"
    },
    {
        "titulo": "Drácula",
        "autor": "Bram Stoker",
        "ano": 1897,
        "genero": "Terror",
        "isbn": "9788594318305",
        "status": "Disponível"
    }
]

def main():
    db = SessionLocal()
    try:
        # Limpar dados existentes
        db.query(models.Livro).delete()
        
        # Inserir os livros
        for livro_data in livros:
            livro = models.Livro(**livro_data)
            if livro_data["status"] == "Emprestado":
                livro.data_emprestimo = date.today()
            db.add(livro)
        
        db.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
