export async function fetchProdutos(orderBy, isAsc, search, categoria, isBaixoEstoque, isVencido) {
    try {
        // TO DO: verificar se o usuario esta logado
        // Solucao: Enviar o token pelo metodo HTTP no header
        //console.log("Requisitando dados da tabela de produtos com os parametros:");
        //console.log({ orderBy, isAsc, search, categoria, isBaixoEstoque, isVencido });

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
                    "categoria": categoria,
                    "isBaixoEstoque": isBaixoEstoque,
                    "isVencido": isVencido
                })
            }
        );

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        const dados = await response.json();
        return dados;
    } catch {
        return { error: "Nao foi possivel ler a tabela de produtos" };
    }
};