const allowedExtensions = ["csv", "xlsx"];
const allowedMimeTypes = [
  "text/csv",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/vnd.ms-excel"
];

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
    const response = await fetch(
      `http://localhost:8000/upload/${tipo}`,
      {
        method: "POST",
        body: formData,
      }
    );
    return await response.json();
  } catch {
    return { error: "Erro ao enviar o arquivo" };
  }
}

export const handleFileSelect = (
  event,
  setFile,
  setFileName,
  setFileInfo
) => {
  const files = event.target.files;

  if (files && files.length > 0) {
    const file = files[0];

    setFile(file);
    setFileName(file.name);

    setFileInfo({
      size: file.size,
      lastModified: new Date(file.lastModified),
      type: file.type,
    });

    return;
  }

  setFile(null);
  setFileName("Nenhum arquivo selecionado");
  setFileInfo(null);
};

