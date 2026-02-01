export async function fetchProdutos(orderBy, isAsc, search, tipo, isBaixoEstoque, isVencido) {
    try {
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
                    "tipo": tipo,
                    "isBaixoEstoque": isBaixoEstoque,
                    "isVencido": isVencido
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        const dados = await response.json();
        console.log(dados)
        return dados;
    } catch {
        return { error: "Nao foi possivel ler a tabela de produtos" };
    }
};