const api_url = import.meta.env.VITE_API_URL;

export const fetchHealth = async () => {

    const response = await fetch(`http://127.0.0.1:8000/admin/health`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) throw new Error("Não foi possível buscar informações de saúde do sistema: Tente novamente mais tarde");

    const dados = await response.json();
    return dados;
}