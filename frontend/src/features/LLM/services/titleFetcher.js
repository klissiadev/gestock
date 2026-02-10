const BASE_URL = "http://127.0.0.1:8000";

const titleCache = {};

export async function fetchTitle( sessionID ) {
    console.log(titleCache)

    if (titleCache[sessionID]) {
        return titleCache[sessionID];
    }


    const response = await fetch(`${BASE_URL}/llm/sessions/${sessionID}/title`,{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
      throw new Error("Erro ao buscar Titulo da sessão");
    }

    const data = await response.json();
    if (data) {
        titleCache[sessionID] = data;
    }

    return data}
;


