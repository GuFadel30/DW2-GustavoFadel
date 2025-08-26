// Configuração da API
const API_URL = 'http://localhost:8000';
const ITEMS_PER_PAGE = 10;

// Estado da aplicação
let currentPage = 1;
let totalPages = 1;
let livrosCache = [];
let sortConfig = JSON.parse(localStorage.getItem('sortConfig')) || {
    field: 'titulo',
    ascending: true
};

// Elementos do DOM
const listaLivros = document.getElementById('listaLivros');
const modalLivro = document.getElementById('modalLivro');
const modalEmprestimo = document.getElementById('modalEmprestimo');
const formLivro = document.getElementById('formLivro');
const formEmprestimo = document.getElementById('formEmprestimo');
const btnNovo = document.getElementById('btnNovo');
const btnCancelar = document.getElementById('btnCancelar');
const btnCancelarEmprestimo = document.getElementById('btnCancelarEmprestimo');
const inputBusca = document.getElementById('busca');
const filtroForm = document.getElementById('filtros');
const btnExportar = document.getElementById('btnExportar');
const sortBtns = {
    titulo: document.getElementById('sortTitulo'),
    ano: document.getElementById('sortAno')
};
const paginationControls = {
    prev: document.getElementById('prevPage'),
    next: document.getElementById('nextPage'),
    current: document.getElementById('currentPage')
};

// Event Listeners
document.addEventListener('DOMContentLoaded', inicializarAplicacao);
btnNovo.addEventListener('click', () => modalLivro.showModal());
btnCancelar.addEventListener('click', () => modalLivro.close());
btnCancelarEmprestimo.addEventListener('click', () => modalEmprestimo.close());
formLivro.addEventListener('submit', handleSubmitLivro);
formEmprestimo.addEventListener('submit', handleEmprestimo);
inputBusca.addEventListener('input', debounce(aplicarFiltros, 300));
filtroForm.addEventListener('change', aplicarFiltros);
btnExportar.addEventListener('click', exportarDados);

// Atalhos de teclado
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        btnNovo.click();
    }
});

// Inicialização
async function inicializarAplicacao() {
    await carregarLivros();
    inicializarOrdenacao();
    aplicarFiltros();
}

// Ordenação
function inicializarOrdenacao() {
    Object.entries(sortBtns).forEach(([field, btn]) => {
        btn.addEventListener('click', () => toggleSort(field));
        if (field === sortConfig.field) {
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
        }
    });
}

function toggleSort(field) {
    if (sortConfig.field === field) {
        sortConfig.ascending = !sortConfig.ascending;
    } else {
        sortConfig.field = field;
        sortConfig.ascending = true;
    }
    
    localStorage.setItem('sortConfig', JSON.stringify(sortConfig));
    aplicarFiltros();
    
    // Atualizar UI
    Object.values(sortBtns).forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
    });
    sortBtns[field].classList.add('active');
    sortBtns[field].setAttribute('aria-pressed', 'true');
}

// Funções de API
async function carregarLivros() {
    try {
        const response = await fetch(`${API_URL}/livros/`);
        if (!response.ok) throw new Error('Erro ao carregar livros');
        livrosCache = await response.json();
    } catch (error) {
        console.error('Erro ao carregar livros:', error);
        alert('Erro ao carregar livros. Verifique se o backend está rodando.');
    }
}

async function handleSubmitLivro(event) {
    event.preventDefault();
    const formData = new FormData(formLivro);
    const livro = Object.fromEntries(formData);

    try {
        const response = await fetch(`${API_URL}/livros/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(livro),
        });

        if (response.ok) {
            modalLivro.close();
            formLivro.reset();
            await carregarLivros();
            aplicarFiltros();
        } else {
            const error = await response.json();
            alert(`Erro ao cadastrar livro: ${error.detail}`);
        }
    } catch (error) {
        console.error('Erro ao cadastrar livro:', error);
        alert('Erro ao cadastrar livro.');
    }
}

async function handleEmprestimo(event) {
    event.preventDefault();
    const livroId = formEmprestimo.dataset.livroId;
    const acao = formEmprestimo.dataset.acao;
    
    try {
        const response = await fetch(`${API_URL}/livros/${livroId}/${acao}`, {
            method: 'POST',
        });

        if (response.ok) {
            modalEmprestimo.close();
            await carregarLivros();
            aplicarFiltros();
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error(`Erro ao ${acao} livro:`, error);
        alert(`Erro ao ${acao} livro.`);
    }
}

// Filtros e Renderização
function aplicarFiltros() {
    const termo = inputBusca.value.toLowerCase();
    const genero = filtroForm.genero.value;
    const ano = filtroForm.ano.value;
    const status = filtroForm.status.value;

    let livrosFiltrados = livrosCache.filter(livro => {
        const matchTermo = !termo || 
            livro.titulo.toLowerCase().includes(termo) || 
            livro.autor.toLowerCase().includes(termo);
        const matchGenero = !genero || livro.genero === genero;
        const matchAno = !ano || livro.ano === parseInt(ano);
        const matchStatus = !status || livro.status === status;

        return matchTermo && matchGenero && matchAno && matchStatus;
    });

    // Ordenação
    livrosFiltrados.sort((a, b) => {
        const valueA = a[sortConfig.field];
        const valueB = b[sortConfig.field];
        const modifier = sortConfig.ascending ? 1 : -1;
        
        return valueA > valueB ? modifier : -modifier;
    });

    // Paginação
    totalPages = Math.ceil(livrosFiltrados.length / ITEMS_PER_PAGE);
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const livrosPaginados = livrosFiltrados.slice(start, start + ITEMS_PER_PAGE);

    renderizarLivros(livrosPaginados);
    atualizarPaginacao();
}

function renderizarLivros(livros) {
    listaLivros.innerHTML = livros.map(livro => `
        <div class="livro-card" tabindex="0">
            <h3 class="livro-titulo">${livro.titulo}</h3>
            <p class="livro-autor">por ${livro.autor}</p>
            <p class="livro-info">Gênero: ${livro.genero}</p>
            <p class="livro-info">Ano: ${livro.ano}</p>
            ${livro.isbn ? `<p class="livro-info">ISBN: ${livro.isbn}</p>` : ''}
            <span class="livro-status status-${livro.status.toLowerCase()}">${livro.status}</span>
            <div class="livro-acoes">
                <button onclick="editarLivro(${livro.id})" aria-label="Editar ${livro.titulo}">Editar</button>
                <button onclick="gerenciarEmprestimo(${livro.id})" 
                    aria-label="${livro.status === 'Disponível' ? 'Emprestar' : 'Devolver'} ${livro.titulo}">
                    ${livro.status === 'Disponível' ? 'Emprestar' : 'Devolver'}
                </button>
                <button onclick="deletarLivro(${livro.id})" aria-label="Excluir ${livro.titulo}">Excluir</button>
            </div>
        </div>
    `).join('');
}

function atualizarPaginacao() {
    paginationControls.current.textContent = currentPage;
    paginationControls.prev.disabled = currentPage === 1;
    paginationControls.next.disabled = currentPage === totalPages;
}

// Utilitários
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function exportarDados() {
    const dados = livrosCache.map(({ id, data_emprestimo, ...livro }) => livro);
    const csv = [
        Object.keys(dados[0]).join(','),
        ...dados.map(item => Object.values(item).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'biblioteca.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
