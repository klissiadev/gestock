// Nome dos fields
export const PRODUCT_HEADER_NAMES = {
    id: "ID",
    nome: "Nome do Produto",
    tipo: "Tipo",
    descricao: "Descrição",
    estoque_atual: "Estoque Atual",
    estoque_minimo: "Estoque Mínimo",
    baixo_estoque: "Estoque Baixo",
    vencido: "Vencido",
    data_validade: "Validade",
    ativo: "Ativo"
};

// Filtros originais
export const INITIAL_FILTERS = {
    searchTerm: "",
    orderBy: "id",
    isAsc: true,
    categoria: "",
    isBaixoEstoque: false,
    isVencido: false
}
