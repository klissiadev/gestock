export const IMPORT_DEFAULT_PARAMS = {
    search_term: "",         // String: busca em nome_arquivo e msg_erro
    status: null,            // String: 'PROCESSANDO', 'CONCLUIDO', etc.
    apenas_erro: false,      // Boolean: se true, filtra automaticamente por 'ERRO'
    periodo: [null, null],   // Array: [data_inicio, data_fim] no formato 'YYYY-MM-DD'
    order_by: "created_at",  // Coluna padrão de ordenação
    direction: "DESC"        // Ordem decrescente (mais recentes primeiro)
};

export const LLMLOGS_DEFAULT_PARAMS = {

};
