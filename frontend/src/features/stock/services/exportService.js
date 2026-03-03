export async function downloadProduct(filters) { 
    try {
        const response = await fetch(
            `http://localhost:8000/views/download/product`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(filters)
            }
        );

        if (!response.ok) throw new Error("Não foi possível realizar a exportação: Tente novamente mais tarde ou avise o adminstrador");

        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = "relatorio.xlsx"; // Nome padrão
        if (contentDisposition && contentDisposition.includes('filename=')) {
            const match = contentDisposition.match(/filename=(.+)/);
            if (match && match[1]) {
                filename = match[1].replace(/['"]/g, '').trim();
            }
        }

        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        
        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        a.remove();

    } catch (error) {
        console.error("Erro técnico:", error);
        throw error;
    }
};

export async function downloadTransactions(filters) { 
    try {
        const response = await fetch(
            `http://localhost:8000/views/download/transaction`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(filters)
            }
        );

        if (!response.ok) throw new Error("Não foi possível realizar a exportação: Tente novamente mais tarde ou avise o adminstrador");

        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = "relatorio.xlsx"; // Nome padrão
        if (contentDisposition && contentDisposition.includes('filename=')) {
            const match = contentDisposition.match(/filename=(.+)/);
            if (match && match[1]) {
                filename = match[1].replace(/['"]/g, '').trim();
            }
        }

        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        
        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        a.remove();

    } catch (error) {
        console.error("Erro técnico:", error);
        throw error;
    }
};
