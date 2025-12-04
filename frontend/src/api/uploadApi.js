// src/api/uploadApi.js

const allowedExtensions = ["csv", "xlsx"];
const allowedMimeTypes = [
  "text/csv",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
];

function validateFile(file) {
  if (!file) return { valid: false, error: "Nenhum arquivo selecionado." };

  const extension = file.name.split(".").pop().toLowerCase();
  const mime = file.type;

  if (!allowedExtensions.includes(extension)) {
    return {
      valid: false,
      error: "Arquivo inválido. Envie apenas CSV ou XLSX.",
    };
  }

  if (mime && !allowedMimeTypes.includes(mime)) {
    return {
      valid: false,
      error: "Tipo MIME inválido. Envie apenas CSV ou XLSX.",
    };
  }

  return { valid: true };
}

export async function uploadFile(file) {
  // validação aqui!
  const validation = validateFile(file);
  if (!validation.valid) {
    return { error: validation.error };
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });

    return await response.json();
  } catch (error) {
    return { error: "Erro ao enviar o arquivo" };
  }
}
