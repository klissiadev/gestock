const BASE_URL = "http://localhost:8001";

/**
 * Busca anomalias a partir de uma data
 * @param {string} dataCorte - formato YYYY-MM-DD
 * @returns {Promise<Array>}
 */
export async function getAnomalies(dataCorte) {
  try {
    console.log(dataCorte);
    const response = await fetch(
      `${BASE_URL}/anomalies?data_corte=${dataCorte}`
    );

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const json = await response.json();

    // padrão: { data: [...], count: number }
    return Array.isArray(json.data) ? json.data : [];

  } catch (error) {
    console.error("Erro ao buscar anomalias:", error);
    return [];
  }
}
