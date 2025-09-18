// Estado da aplicação
const state = {
    livros: [],
    currentPage: 1,
    itemsPerPage: 9,
    sortBy: localStorage.getItem('sortBy') || 'titulo',
    sortOrder: localStorage.getItem('sortOrder') || 'asc',
    filters: {
        search: '',
        genero: '',
        ano: '',
        status: ''
    }
};

// Funções de API
const api = {
    async getLivros(params = {}) {
        try {
            const queryString = new URLSearchParams(params).toString();
            const response = await fetch(`http://127.0.0.1:8000/livros?${queryString}`);
            if (!response.ok) throw new Error('Erro ao buscar livros');
            return response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    },

    async createLivro(livro) {
        try {
            const response = await fetch('http://localhost:8000/livros', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(livro)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro ao criar livro');
            }
            
            return response.json();
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    },

    async updateLivro(id, livro) {
        const response = await fetch(`http://localhost:8000/livros/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(livro)
        });
        if (!response.ok) throw new Error('Erro ao atualizar livro');
        return response.json();
    },

    async deleteLivro(id) {
        const response = await fetch(`http://localhost:8000/livros/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Erro ao deletar livro');
    },

    async emprestarLivro(id) {
        const response = await fetch(`http://localhost:8000/livros/${id}/emprestar`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Erro ao emprestar livro');
        return response.json();
    },

    async devolverLivro(id) {
        const response = await fetch(`http://localhost:8000/livros/${id}/devolver`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Erro ao devolver livro');
        return response.json();
    }
};

// Funções de renderização
function renderLivros(livros) {
    const container = document.getElementById('listaLivros');
    container.innerHTML = '';

    if (livros.length === 0) {
        container.innerHTML = '<p class="no-results">Nenhum livro encontrado</p>';
        return;
    }

    livros.forEach(livro => {
        const card = document.createElement('div');
        card.className = 'book-card';
        card.dataset.status = livro.status;
        card.innerHTML = `
            <div class="book-info">
                <h3>${livro.titulo}</h3>
                <p><strong>Autor:</strong> ${livro.autor}</p>
                <p><strong>Ano:</strong> ${livro.ano}</p>
                <p><strong>Gênero:</strong> ${livro.genero}</p>
                <p class="status-${livro.status.toLowerCase()}">
                    <strong>Status:</strong> ${livro.status}
                </p>
            </div>
            <div class="card-actions">
                <button onclick="handleEmprestimo(${livro.id})" 
                        class="btn-emprestar"
                        aria-label="${livro.status === 'Disponível' ? 'Emprestar' : 'Devolver'} ${livro.titulo}">
                    ${livro.status === 'Disponível' ? 'Emprestar' : 'Devolver'}
                </button>
                <button onclick="handleEdit(${livro.id})" 
                        class="btn-editar"
                        aria-label="Editar ${livro.titulo}">
                    Editar
                </button>
                <button onclick="handleDelete(${livro.id})" 
                        class="btn-excluir"
                        aria-label="Excluir ${livro.titulo}">
                    Excluir
                </button>
            </div>
        `;
        container.appendChild(card);
    });

    updatePagination();
}

// Funções de filtro e ordenação
function filterLivros() {
    let filtered = [...state.livros];

    if (state.filters.search) {
        const search = state.filters.search.toLowerCase();
        filtered = filtered.filter(livro => 
            livro.titulo.toLowerCase().includes(search) ||
            livro.autor.toLowerCase().includes(search)
        );
    }

    if (state.filters.genero) {
        filtered = filtered.filter(livro => livro.genero === state.filters.genero);
    }

    if (state.filters.ano) {
        filtered = filtered.filter(livro => livro.ano === parseInt(state.filters.ano));
    }

    if (state.filters.status) {
        filtered = filtered.filter(livro => livro.status === state.filters.status);
    }

    filtered.sort((a, b) => {
        const order = state.sortOrder === 'asc' ? 1 : -1;
        return a[state.sortBy] > b[state.sortBy] ? order : -order;
    });

    const start = (state.currentPage - 1) * state.itemsPerPage;
    const paginatedItems = filtered.slice(start, start + state.itemsPerPage);

    renderLivros(paginatedItems);
}

// Event Handlers
async function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const livro = Object.fromEntries(formData);
    
    // Converter o ano para número
    if (livro.ano) {
        livro.ano = parseInt(livro.ano);
    }

    // Adicionar status inicial
    livro.status = 'Disponível';

    try {
        const response = await api.createLivro(livro);
        if (response) {
            await loadLivros();
            document.getElementById('modalLivro').close();
            event.target.reset();
        }
    } catch (error) {
        console.error('Erro ao criar livro:', error);
        alert('Erro ao criar livro: ' + error.message);
    }
}

async function handleEmprestimo(id) {
    const livro = state.livros.find(l => l.id === id);
    if (!livro) return;

    try {
        if (livro.status === 'Disponível') {
            await api.emprestarLivro(id);
        } else {
            await api.devolverLivro(id);
        }
        await loadLivros();
    } catch (error) {
        alert(error.message);
    }
}

async function handleDelete(id) {
    if (!confirm('Tem certeza que deseja excluir este livro?')) return;

    try {
        await api.deleteLivro(id);
        await loadLivros();
    } catch (error) {
        alert(error.message);
    }
}

function handleEdit(id) {
    const livro = state.livros.find(l => l.id === id);
    if (!livro) return;

    const form = document.getElementById('formLivro');
    for (const [key, value] of Object.entries(livro)) {
        const input = form.elements[key];
        if (input) input.value = value;
    }

    modalLivro.showModal();
}

// Exportação
function exportData(format = 'json') {
    const data = state.livros;
    let content, filename;

    if (format === 'csv') {
        const headers = ['titulo', 'autor', 'ano', 'genero', 'isbn', 'status'].join(',');
        const rows = data.map(livro => 
            [livro.titulo, livro.autor, livro.ano, livro.genero, livro.isbn, livro.status].join(',')
        );
        content = [headers, ...rows].join('\n');
        filename = 'livros.csv';
    } else {
        content = JSON.stringify(data, null, 2);
        filename = 'livros.json';
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Inicialização
async function loadLivros() {
    try {
        const livros = await api.getLivros();
        state.livros = livros;
        filterLivros();
    } catch (error) {
        alert('Erro ao carregar livros: ' + error.message);
    }
}

function updatePagination() {
    document.getElementById('currentPage').textContent = state.currentPage;
    const totalPages = Math.ceil(state.livros.length / state.itemsPerPage);
    
    document.getElementById('prevPage').disabled = state.currentPage === 1;
    document.getElementById('nextPage').disabled = state.currentPage === totalPages;
}

// Event Listeners
// Função para gerenciar o tema
function initTheme() {
    const btnTema = document.getElementById('btnTema');
    const root = document.documentElement;
    
    // Verifica se há um tema salvo no localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        root.dataset.theme = savedTheme;
    }

    // Adiciona o evento de clique para alternar o tema
    btnTema.addEventListener('click', () => {
        const currentTheme = root.dataset.theme;
        const newTheme = currentTheme === 'light' ? '' : 'light';
        root.dataset.theme = newTheme;
        localStorage.setItem('theme', newTheme);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    // Carregar livros iniciais
    loadLivros();

    // Form de novo livro
    const formLivro = document.getElementById('formLivro');
    formLivro.addEventListener('submit', handleSubmit);

    // Filtros
    const filtros = document.getElementById('filtros');
    filtros.addEventListener('change', e => {
        state.filters[e.target.name] = e.target.value;
        state.currentPage = 1;
        filterLivros();
    });

    // Busca
    const busca = document.getElementById('busca');
    busca.addEventListener('input', e => {
        state.filters.search = e.target.value;
        state.currentPage = 1;
        filterLivros();
    });

    // Ordenação
    document.getElementById('sortTitulo').addEventListener('click', () => {
        state.sortBy = 'titulo';
        state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
        localStorage.setItem('sortBy', state.sortBy);
        localStorage.setItem('sortOrder', state.sortOrder);
        filterLivros();
    });

    document.getElementById('sortAno').addEventListener('click', () => {
        state.sortBy = 'ano';
        state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
        localStorage.setItem('sortBy', state.sortBy);
        localStorage.setItem('sortOrder', state.sortOrder);
        filterLivros();
    });

    // Paginação
    document.getElementById('prevPage').addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            filterLivros();
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        const totalPages = Math.ceil(state.livros.length / state.itemsPerPage);
        if (state.currentPage < totalPages) {
            state.currentPage++;
            filterLivros();
        }
    });

    // Modal de novo livro
    const modalLivro = document.getElementById('modalLivro');
    const btnNovo = document.getElementById('btnNovo');
    const btnCancelar = document.getElementById('btnCancelar');

    btnNovo.addEventListener('click', () => {
        formLivro.reset();
        document.getElementById('modalTitle').textContent = 'Cadastrar Livro';
        formLivro.dataset.mode = 'create';
        modalLivro.showModal();
    });

    btnCancelar.addEventListener('click', () => {
        modalLivro.close();
    });

    // Exportação
    document.getElementById('btnExportar').addEventListener('click', () => {
        const format = confirm('Clique OK para exportar como CSV ou Cancelar para JSON') ? 'csv' : 'json';
        exportData(format);
    });

    // Atalho Alt+N
    document.addEventListener('keydown', e => {
        if (e.altKey && e.key === 'n') {
            e.preventDefault();
            btnNovo.click();
        }
    });
});
