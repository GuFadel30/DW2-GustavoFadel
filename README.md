# Biblioteca Escolar - Gustavo Fadel

Sistema de gerenciamento de biblioteca escolar com frontend moderno e API REST.

## Screenshots

![Tela Principal](screenshots/main.png)
![Modal de Novo Livro](screenshots/new-book.png)
![Modal de Empréstimo](screenshots/loan.png)

## Características

### Frontend
- Interface moderna com tema escuro
- Filtros combinados (gênero, ano, texto)
- Ordenação persistente
- Paginação
- Exportação CSV/JSON
- Acessibilidade (ARIA, atalhos)
- Validações de formulário

### Backend
- API REST com FastAPI
- Banco SQLite
- Validações de regras de negócio
- Seed script com 15+ livros

## Tecnologias

- Frontend: HTML5, CSS3 (Grid/Flex), JavaScript ES6+
- Backend: Python, FastAPI, SQLAlchemy
- Banco de Dados: SQLite

## Como Executar

1. Clone o repositório
   ```bash
   git clone https://github.com/GuFadel30/dw2-gustavo-fadel.git
   cd dw2-gustavo-fadel
   ```

2. Configure o ambiente Python
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   cd backend
   pip install -r requirements.txt
   ```

3. Inicialize o banco
   ```bash
   python seed.py
   ```

4. Inicie o servidor
   ```bash
   uvicorn app:app --reload
   ```

5. Sirva o frontend
   ```bash
   cd ../frontend
   python -m http.server 5500
   ```

6. Acesse http://localhost:5500

## Atalhos

- `Alt + N`: Abre modal de novo livro
- `Enter` em campos: Aplica filtros
- `Esc` em modais: Fecha

## Validações

### Frontend
- Título único
- ISBN válido (10-13 dígitos)
- Ano entre 1900-2025
- Campos obrigatórios
- Status correto para empréstimo

### Backend
- Validação de dados
- Regras de negócio
- Integridade referencial

## Autor

Gustavo Fadel - [@GuFadel30](https://github.com/GuFadel30)
