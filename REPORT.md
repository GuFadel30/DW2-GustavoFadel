# Relatório do Projeto

## Estrutura do Projeto

O projeto foi organizado em duas partes principais:

### Backend (FastAPI)
- `app.py`: Contém as rotas da API e a lógica principal
- `models.py`: Define os modelos de dados usando SQLAlchemy e Pydantic
- `database.py`: Configuração da conexão com o banco de dados SQLite
- `seed.py`: Script para popular o banco com dados iniciais
- `requirements.txt`: Lista de dependências Python

### Frontend (HTML/CSS/JavaScript)
- `index.html`: Interface do usuário
- `styles.css`: Estilos da aplicação
- `scripts.js`: Lógica do cliente e interação com a API

## Funcionalidades Implementadas

1. **Gerenciamento de Livros**
   - Listagem de todos os livros
   - Cadastro de novos livros
   - Atualização de informações
   - Exclusão de livros
   - Busca por título ou autor

2. **Modelo de Dados**
   - Título
   - Autor
   - Ano de Publicação
   - Editora
   - ISBN
   - Status (Disponível, Emprestado, Em Manutenção)

3. **Interface**
   - Design responsivo
   - Modal para cadastro/edição
   - Busca em tempo real
   - Feedback visual de status
   - Confirmação para exclusão

## Tecnologias Utilizadas

### Backend
- FastAPI para API REST
- SQLAlchemy para ORM
- SQLite para banco de dados
- Pydantic para validação de dados

### Frontend
- HTML5 para estrutura
- CSS3 para estilização
- JavaScript puro para interatividade
- Fetch API para requisições HTTP

## Pontos de Melhoria Futura

1. **Segurança**
   - Implementar autenticação
   - Adicionar autorização baseada em papéis
   - Validação mais robusta de dados

2. **Funcionalidades**
   - Sistema de empréstimos
   - Histórico de movimentações
   - Categorização de livros
   - Relatórios estatísticos

3. **Interface**
   - Tema escuro
   - Mais filtros de busca
   - Paginação da lista
   - Upload de capas de livros

4. **Técnico**
   - Testes automatizados
   - Cache de dados
   - Logging de operações
   - Backup automático
