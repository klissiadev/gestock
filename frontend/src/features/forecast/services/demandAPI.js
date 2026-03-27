export async function getAnomalies(dataCorte) {
    const url = `http://127.0.0.1:8000/forecasting/anomalies?data_corte=${dataCorte}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erro na requisição: Status ${response.status}`);
        }

        const resultado = await response.json();

        console.log(`Encontradas ${resultado.count} anomalias.`);
        console.log("Dados:", resultado.data);

        return resultado;

    } catch (error) {
        console.error("Falha ao buscar as anomalias:", error);
        return null;
    }
}