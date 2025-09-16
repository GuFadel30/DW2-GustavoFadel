# Relatório do Projeto

## Arquitetura

### Frontend
- HTML5 semântico com acessibilidade ARIA
- CSS Grid/Flex para layout responsivo
- JavaScript ES6+ sem frameworks
- LocalStorage para persistência de preferências
- Fetch API para comunicação REST

### Backend
- FastAPI com SQLAlchemy
- SQLite como banco de dados
- Arquitetura em camadas:
  - Routes (app.py)
  - Models (models.py)
  - Database (database.py)

## Tecnologias Utilizadas

### Frontend
- HTML5
- CSS3 (Grid, Flexbox, Custom Properties)
- JavaScript ES6+ (Modules, Async/Await)
- Web Storage API
- Dialog Element
- Fetch API

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy ORM
- SQLite
- Uvicorn ASGI Server

## Prompts Copilot

1. Estrutura inicial:
   ```
   Crie a estrutura de um projeto fullstack com:
   - Frontend (HTML/CSS/JS)
   - Backend (FastAPI/SQLite)
   - Documentação (README/REPORT)
   ```

2. Frontend:
   ```
   Implemente uma interface moderna com:
   - Tema escuro
   - Grid/Flex layout
   - Modais nativos
   - Acessibilidade
   ```

3. Backend:
   ```
   Configure uma API REST com:
   - CRUD de livros
   - Validações
   - Regras de negócio
   - Seed script
   ```

## Peculiaridades Implementadas

### Acessibilidade
- ARIA labels e roles
- Feedback de status
- Atalhos de teclado
- Foco visível
- Contraste adequado

### Seed Script
- 15+ livros diversos
- Validação de duplicatas
- Dados realistas
- Execução idempotente

### Export
- Formato CSV e JSON
- Filtros aplicados
- Download automático
- Headers corretos

## Validações

### Frontend
```javascript
// Título único
const titulo = form.titulo.value;
const exists = livros.some(l => l.titulo === titulo);
if (exists) throw new Error('Título já existe');

// ISBN
const isbn = form.isbn.value;
if (isbn && !/^[0-9-]{10,13}$/.test(isbn)) {
    throw new Error('ISBN inválido');
}

// Ano
const ano = parseInt(form.ano.value);
if (ano < 1900 || ano > 2025) {
    throw new Error('Ano inválido');
}
```

### Backend
```python
# Validar título único
existing = db.query(Book).filter(Book.titulo == titulo).first()
if existing:
    raise HTTPException(status_code=400, detail="Título já existe")

# Validar empréstimo
if livro.status != "Disponível":
    raise HTTPException(status_code=400, detail="Livro não disponível")
```

## Como Executar

1. Ambiente:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Backend:
   ```bash
   cd backend
   python seed.py
   uvicorn app:app --reload
   ```

3. Frontend:
   ```bash
   cd frontend
   python -m http.server 5500
   ```

## Limitações e Melhorias

### Limitações Atuais
- Sem autenticação
- Sem histórico de empréstimos
- Sem backup automático
- Interface não é PWA

### Melhorias Futuras
- Sistema de login
- Histórico completo
- Backup na nuvem
- Modo offline
- Notificações
- Relatórios avançados
