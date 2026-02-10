from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.report_prompts import PROMPTS



# =========================
# Schemas
# =========================

class ReportInput(BaseModel):
    report_type: str
    tipo: str
    dados: Any
    parametros: Optional[Dict[str, Any]] = Field(default_factory=dict)


# =========================
# Agent
# =========================

class ReportAgent:

    PROMPT_VERSION = "v2.0"

    EMPTY_RESPONSE = (
        "Não há informação disponível no sistema para gerar este relatório."
    )

    def __init__(self, model: ChatOllama):
        self.model = model
        print("ReportAgent usando modelo:", self.model.model)

        self.system_prompt = SystemMessage(
            content=self._build_system_prompt()
        )

    # --------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------

    def _build_system_prompt(self) -> str:
        return f"""
    Você é responsável por gerar relatórios OFICIAIS do sistema Gestock.

    VERSÃO DO PROMPT: {self.PROMPT_VERSION}

    REGRAS ABSOLUTAS:

    1. Utilize EXCLUSIVAMENTE os dados recebidos.
    2. Nunca realize cálculos ou classificações adicionais.
    3. Nunca interprete dados.
    4. Nunca gere conclusões.
    5. Nunca reorganize ou agrupe registros.
    6. Nunca adicione recomendações.
    7. Nunca invente informações.

    FORMATO DO RELATÓRIO:

    - Título do relatório
    - Parâmetros utilizados (se existirem)
    - Listagem completa dos registros exatamente como recebidos
    - Metadados (se existirem)

    Se algum campo estiver ausente, declare explicitamente:

    "Dado não disponível nos registros fornecidos."

    O conteúdo gerado é considerado documento oficial do sistema.
    """.strip()


    # --------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------

    def _get_prompt(self, report_type: str) -> str:
        return PROMPTS.get(report_type, "Relatório não configurado.")

    # --------------------------------------------------
    # EXECUÇÃO
    # --------------------------------------------------
    async def gerar(self, report_input: ReportInput):

        registros = (
            report_input.dados.get("registros")
            or report_input.dados.get("data")
            or []
        )
        
        metadata = report_input.dados.get("metadata", {})

        if not registros:
            return self.EMPTY_RESPONSE

        return await self.generate_report(
            report_type=report_input.report_type,
            dados=registros,
            parametros=report_input.parametros,
            metadata=metadata
        )

    async def generate_report(
        self,
        report_type: str,
        dados: list,
        parametros: dict,
        metadata: dict | None = None
    ):
        print("TOTAL DADOS:", len(dados))
        print("REPORT TYPE:", report_type)
        prompt_template = self._get_prompt(report_type)

        prompt = prompt_template.format(
            dados=dados,
            parametros=parametros,
            metadata=metadata or {},
            total_items=len(dados)
        )

        messages = [
            self.system_prompt,
            HumanMessage(content=prompt)
        ]

        response = await self.model.ainvoke(messages)

        return response.content or self.EMPTY_RESPONSE
