export async function fetchMovimentacoes(orderBy, isAsc, search) {
    try {
        console.log("Requisitando dados da tabela de movimentacoes com os parametros:");
        console.log({ orderBy, isAsc, search });
        const response = await fetch(
            `http://localhost:8000/views/moviment`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "orderBy": orderBy,
                    "isAsc": isAsc,
                    "search": search,
                })
            }
        );
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }

        const dados = await response.json();
        return dados;

    } catch {
        return { error: "Nao foi possivel ler a tabela de movimentacoes" };
    }
};