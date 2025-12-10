import { useState } from "react";
import { uploadFile } from "../api/uploadApi";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Selecione um arquivo");
      return;
    }

    setLoading(true);
    const result = await uploadFile(file);
    setResponse(result);
    setLoading(false);
  };

  /* Posição temporaria da função de mailtrigger */
  const handleMailTrigger = async () => {
    const response = await fetch("http://localhost:8000/triggerMail/", { method: "POST" });
    if (!response.ok) throw new Error("Erro ao pedir email");
    const data = await response.json();
    console.log("Resposta do servidor:", data);
  };

  


  const container = {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",

    display: "flex",
    justifyContent: "center",
    alignItems: "center",

    background: "#eef2f7",
    fontFamily: "Arial, sans-serif",
  };

  const card = {
    background: "#fff",
    padding: "30px",
    width: "380px",
    borderRadius: "14px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
    textAlign: "center",
  };

  const title = {
    fontSize: "22px",
    fontWeight: "bold",
    marginBottom: "20px",
    color: "#333",
  };

  const fileInput = {
    width: "100%",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    background: "#fafafa",
    marginBottom: "20px",
    cursor: "pointer",
  };

  const button = {
    width: "100%",
    padding: "12px",
    background: loading ? "#888" : "#0066ff",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "0.3s",
  };

  const responseBox = {
    background: "#000",
    padding: "15px",
    borderRadius: "8px",
    marginTop: "20px",
    whiteSpace: "pre-wrap",
    textAlign: "left",
    fontSize: "14px",
  };

  return (
    <div style={container}>
      <div style={card}>
        <h1 style={title}>Upload de Planilha</h1>

        <input
          type="file"
          style={fileInput}
          accept=".csv, .xlsx"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button style={button} onClick={handleUpload} disabled={loading}>
          {loading ? "Enviando..." : "Enviar"}
        </button>

        {response && (
          <pre style={responseBox}>{JSON.stringify(response, null, 2)}</pre>
        )}

        <p>
          <br />
          <hr />
          <br />
        </p>
        <button style={button} onClick={handleMailTrigger}>
          Disparar E-mails (testandinho)
        </button>
      </div>
    </div>
  );
}
