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

