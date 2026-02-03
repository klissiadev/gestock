import { useState } from "react";
import { uploadFile, handleFileSelect } from "../services/uploadFile"

export const useFileUpload = (initialTipo = "produtos") => {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState("Nenhum arquivo selecionado");
    const [tipo, setTipo] = useState(initialTipo);
    const [fileInfo, setFileInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    // Dentro do useFileUpload.js
    const handleFile = (selectedFile) => {
        if (selectedFile) {
            setFile(selectedFile);
            setFileName(selectedFile.name);
            setFileInfo({
                size: selectedFile.size,
                lastModified: new Date(selectedFile.lastModified),
                type: selectedFile.type,
            });
            setError(null);
        }
    };

    // Para o input tradicional (clique no botão)
    const onFileChange = (event) => {
        const file = event.target.files[0];
        handleFile(file);
    };

    // Para o DragBox (drop direto)
    const onDropSelect = (file) => {
        handleFile(file);
    };

    const handleTypeChange = (newType) => {
        setTipo(newType);
    };

    const executeUpload = async () => {
        setLoading(true);
        setError(null);

        const result = await uploadFile(file, tipo);

        if (result.error) {
            setError(result.error);
        } else {
            setResponse(result);
        }

        setLoading(false);
    };

    const clear = () => {
        setFile(null);
        setFileName("Nenhum arquivo selecionado");
        setFileInfo(null);
        setResponse(null);
        setError(null);
    };

    return {
        file,
        fileName,
        fileInfo,
        tipo,
        loading,
        response,
        error,
        onFileChange,
        onDropSelect,
        handleTypeChange,
        executeUpload,
        clear,
    };
};