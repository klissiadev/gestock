const BASE_URL = "http://localhost:8000";
const allowedExtensions = ["csv", "xlsx"];
const allowedMimeTypes = [
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel"
];

// FETCH GERAL 
export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const headers = {
        ...(token && { "Authorization": `Bearer ${token}` }),
        ...options.headers,
    };

    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

    if (!response.ok) {
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = "/";
            throw new Error("Sessão expirada");
        }
        let backendError = "";
        try {
            const errorData = await response.json();
            if (errorData.detail) {
                backendError = errorData.detail; // Captura "Arquivo duplicado. Este arquivo já foi importado."
            }
        } catch (e) {
            // ignora
        }

        throw new Error(backendError || `Erro na API: ${response.statusText}`);
    }

    return response;
}


//
function validateFile(file) {
    if (!file) return { valid: false, error: "Nenhum arquivo selecionado." };

    const extension = file.name.split(".").pop().toLowerCase();
    const mime = file.type;

    console.log("Validando arquivo:", { extension, mime });
    console.log("Permitidos MIME: ", allowedMimeTypes);

    if (!allowedExtensions.includes(extension)) {
        return { valid: false, error: "Envie apenas CSV ou XLSX." };
    }

    if (mime && !allowedMimeTypes.includes(mime)) {
        return { valid: false, error: "Tipo MIME inválido." };
    }

    return { valid: true };
}

export async function uploadFile(file, tipo) {
    const validation = validateFile(file);
    if (!validation.valid) {
        return { error: validation.error };
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await apiFetch(`/upload/${tipo}`, {
            method: "POST",
            body: formData,
        });
        return await response.json();
    } catch (err) {
        console.log("Erro capturado:", err.message);
        return {error: err.message || "Erro de conexão ao enviar o arquivo." };
    }
}


