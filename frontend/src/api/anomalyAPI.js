const BASE_URL = "http://localhost:8000";

/**
 * Busca anomalias a partir de uma data
 * @param {string} dataCorte - formato YYYY-MM-DD
 * @returns {Promise<Array>}
 */
export async function getAnomalies(dataCorte) {
  try {
    const response = await fetch(
      `${BASE_URL}/anomalies?data_corte=${dataCorte}`
    );

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const json = await response.json();

    // padrão: { data: [...], count: number }
    return json.data;

  } catch (error) {
    console.error("Erro ao buscar anomalias:", error);
    return [];
  }
}
