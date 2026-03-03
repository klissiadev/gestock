export async function fetchMovimentacoes(filters) {
    try {
        const response = await fetch(
            `http://localhost:8000/views/moviment`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(filters)
            }
        );
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }

        const dados = await response.json();
        return dados;

    } catch {
        return { error: "Nao foi possivel ler a tabela de movimentações" };
    }
};