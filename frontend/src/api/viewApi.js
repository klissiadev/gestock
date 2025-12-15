// frontend/src/api/viewApi.js
// Funcoes para interagir com a API de visualizacao de dados


export async function handlePTable(orderBy, isAsc, search, categoria) {
    try {
        // TO DO: verificar se o usuario esta logado
        // Solucao: Enviar o token pelo metodo HTTP no header
        const response = await fetch(
            `http://localhost:8000/views/product`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "orderBy": orderBy,
                    "isAsc": isAsc,
                    "search": search,
                    "categoria": categoria
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        const dados = await response.json();
        console.log(dados);
        return dados;
    } catch {
        return { error: "Nao foi possivel ler a tabela de produtos" };
    }
};

export async function handleMTable(orderBy, isAsc, search, tipoMov) {
    try {
        const response = await fetch(
            `http://localhost:8000/views/movimentacao`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "orderBy": orderBy,
                    "isAsc": isAsc,
                    "search": search,
                    "tipoMov": tipoMov
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }

        const dados = await response.json();
        // console.log(dados);
        return dados;

    } catch {
        return { error: "Nao foi possivel ler a tabela de movimentacoes" };
    }
}