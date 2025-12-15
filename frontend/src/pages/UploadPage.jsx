import { useState } from "react";
import { uploadFile,handleFileSelect } from "../api/uploadApi";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("Nenhum arquivo selecionado");
  const [tipo, setTipo] = useState("Produto");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Selecione um arquivo");
      return;
    }

    setLoading(true);
    const result = await uploadFile(file, tipo);
    setResponse(result);
    setLoading(false);
  };

  const container = {
    position: "fixed",
    inset: 0,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#eef2f7",
    fontFamily: "Arial, sans-serif",
  };

  const card = {
    background: "#fff",
    padding: "30px",
    width: "420px",
    borderRadius: "14px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
    textAlign: "center",
  };


  const input = {
    width: "90%",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    marginBottom: "15px",
  };

  const button = {
    width: "90%",
    padding: "12px",
    background: loading ? "#888" : "#0066ff",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer",
  };

  const responseBox = {
    background: "#000",
    color: "#0f0",
    padding: "15px",
    borderRadius: "8px",
    marginTop: "20px",
    whiteSpace: "pre-wrap",
    textAlign: "left",
    fontSize: "14px",
  };

  const h2 = {
    color: "#0066ff"
  };

  return (
    <div style={container}>
      <div style={card}>
        <h2 style={h2}>Upload de Planilha</h2>

        <select
          style={input}
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
        >
          <option value="Produto">Produto</option>
          <option value="Movimentacao">Movimentação</option>
        </select>

        <input
          type="file"
          style={input}
          accept=".csv, .xlsx"
          onChange={(e) => handleFileSelect(e, setFile, setFileName, setFileInfo)}
        />

        <p style={{color:'#000'}}>{fileName}</p>

        {fileInfo && (
          <div style={{ fontSize: "13px", color: "#555", marginBottom: "10px" }}>
            <div>Tamanho: {(fileInfo.size / 1024).toFixed(2)} KB</div>
            <div>
              Última modificação:{" "}
              {fileInfo.lastModified.toLocaleString("pt-BR")}
            </div>
          </div>
        )}

        <button style={button} onClick={handleUpload} disabled={loading}>
          {loading ? "Enviando..." : "Enviar"}
        </button>

        {response && (
          <pre style={responseBox}>
            {JSON.stringify(response, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
