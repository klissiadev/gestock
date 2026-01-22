// frontend/src/api/eventApi.js

export async function criarEventoNotificacao(evento) {
  try {
    const response = await fetch("http://localhost:8000/eventos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(evento),
    });

    if (!response.ok) {
      throw new Error("Erro ao criar evento");
    }

    return await response.json();
  } catch (error) {
    console.error("Erro ao enviar evento:", error);
    return null;
  }
}
