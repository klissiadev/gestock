export async function sendCredencials(email, password) {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    const response = await fetch('http://127.0.0.1:8000/auth/login',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: params
        }
    );

    if (!response.ok) {
        const errorBody = await response.json();
        alert(errorBody.detail);
        return;
    }

    const dados = await response.json();
    return dados;
    // Dados é um dict com
    // access_token e token_type
};

export async function registerUser(nome, email, senha, token=null) {
    const response = await fetch('http://127.0.0.1:8000/auth/register',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                "nome": nome,
                "email": email,
                "password": senha, 
            })
        });

    const dados = await response.json();

    if (!response.ok) {
        throw new Error(dados.detail || "Erro ao registrar usuário");
    }

    return dados;

};
