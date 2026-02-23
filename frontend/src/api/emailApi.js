
export async function handleMailTrigger () {
    const response = await fetch("http://localhost:8000/triggerMail/", { method: "POST" });
    if (!response.ok) throw new Error("Erro ao pedir email");
  };