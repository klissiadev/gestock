// Função utilitária para extrair dados de um JSON incompleto
export const parsePartialReport = (content) => {
  if (!content || !content.trim().startsWith('{')) return null;

  try {
    // Tenta o parse normal primeiro (para quando estiver completo)
    const fullParse = JSON.parse(content);
    if (fullParse.type === "REPORT_ACTION") return fullParse;
  } catch (e) {
    // Se falhar, tentamos extrair o que dá via Regex ou busca de string
    const reportTypeMatch = content.match(/"report_type":\s*"([^"]+)"/);
    const reportType = reportTypeMatch ? reportTypeMatch[1] : null;

    if (!reportType || !content.includes('"type": "REPORT_ACTION"')) return null;

    // Localiza o início da array de dados: "dados": [
    const dadosStartIndex = content.indexOf('"dados": [');
    if (dadosStartIndex === -1) {
      return { type: "REPORT_ACTION", report_type: reportType, payload: { dados: [] }, isPartial: true };
    }

    // Extrai o conteúdo dentro do array de dados
    let dadosPart = content.substring(dadosStartIndex + 10);
    
    // Tenta encontrar todos os blocos de strings completas dentro do array parcial
    // Procura por padrões "1. Produto: ...", "2. Produto: ..."
    const items = [];
    const itemRegex = /"([^"]+)"/g;
    let match;
    while ((match = itemRegex.exec(dadosPart)) !== null) {
      items.push(match[1].replace(/\\n/g, '\n'));
    }

    return {
      type: "REPORT_ACTION",
      report_type: reportType,
      payload: { 
        dados: items,
        total_items: items.length // Opcional: mostrar contagem parcial
      },
      isPartial: true
    };
  }
  return null;
};