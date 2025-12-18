import { useState } from "react";
import { uploadFile, handleFileSelect } from "../api/uploadApi";
import { handleMailTrigger } from "../api/emailApi";
import { ToastContainer, toast } from 'react-toastify';

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

  const handleMail = async () => {
    try {
      handleMailTrigger();
      toast.success("E-mails agendados para envio");
    } catch (error) {
      toast.error("Erro ao agendar envio de e-mails");
    }
  };

  /* ===== STYLES ===== */

  const container = {
    position: "fixed",
    inset: 0,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #eef2f7, #dbe4f0)",
    fontFamily: "Inter, Arial, sans-serif",
    padding: "20px",
  };

  const card = {
    background: "#fff",
    padding: "32px",
    width: "440px",
    borderRadius: "18px",
    boxShadow: "0 12px 30px rgba(0,0,0,0.12)",
  };

  const title = {
    textAlign: "center",
    color: "#1e40af",
    marginBottom: "8px",
  };

  const subtitle = {
    textAlign: "center",
    fontSize: "14px",
    color: "#64748b",
    marginBottom: "24px",
  };

  const select = {
    width: "100%",
    padding: "10px",
    borderRadius: "10px",
    border: "1px solid #cbd5e1",
    marginBottom: "16px",
    fontSize: "14px",
  };

  const fileInfoBox = {
    fontSize: "13px",
    color: "#475569",
    background: "#f1f5f9",
    padding: "10px 14px",
    borderRadius: "10px",
    marginBottom: "16px",
  };

  const button = {
    width: "100%",
    padding: "14px",
    background: loading ? "#94a3b8" : "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "12px",
    fontSize: "16px",
    fontWeight: "600",
    cursor: loading ? "not-allowed" : "pointer",
    transition: "0.2s",
  };

  const responseBox = {
    background: "#020617",
    color: "#4ade80",
    padding: "16px",
    borderRadius: "12px",
    marginTop: "20px",
    whiteSpace: "pre-wrap",
    fontSize: "13px",
    maxHeight: "200px",
    overflow: "auto",
  };

  return (
    <div style={container}>
      <ToastContainer />
      <div style={card}>
        <h2 style={title}>Upload de Planilha</h2>
        <p style={subtitle}>
          Envie arquivos <strong>.csv</strong> ou <strong>.xlsx</strong>
        </p>

        <select
          style={select}
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
        >
          <option value="Produto">Produto</option>
          <option value="Movimentacao">Movimentação</option>
        </select>

        <input
          type="file"
          accept=".csv, .xlsx"
          style={{
            width: "95%",
            padding: "10px",
            borderRadius: "10px",
            border: "1px solid #cbd5e1",
            marginBottom: "8px",
            fontSize: "14px",
          }}
          onChange={(e) =>
            handleFileSelect(e, setFile, setFileName, setFileInfo)
          }
        />

        <p
          style={{
            fontSize: "13px",
            color: file ? "#1e293b" : "#94a3b8",
            marginBottom: "12px",
          }}
        >
          {fileName}
        </p>

        {fileInfo && (
          <div style={fileInfoBox}>
            <div>Tamanho: {(fileInfo.size / 1024).toFixed(2)} KB</div>
            <div>
              Última modificação:{" "}
              {fileInfo.lastModified.toLocaleString("pt-BR")}
            </div>
          </div>
        )}

        <button style={button} onClick={handleUpload} disabled={loading}>
          {loading ? "Enviando arquivo..." : "Enviar arquivo"}
        </button>

        {response && (
          <pre style={responseBox}>
            {JSON.stringify(response, null, 2)}
          </pre>
        )}

        <hr style={{ margin: '30px' }} />

        <button style={button} onClick={handleMail} disabled={loading}>
          Disparar E-mails (Teste)
        </button>
      </div>
    </div>
  );
}
