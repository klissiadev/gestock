import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from prompts.report_prompts import PROMPTS
from llm_module.formatters.formatter_factory import FORMATTERS


# =========================
# Schemas
# =========================

class ReportInput(BaseModel):
    report_type: str
    dados: Any
    parametros: Optional[Dict[str, Any]] = Field(default_factory=dict)


# =========================
# Agent
# =========================

class ReportAgent:

    PROMPT_VERSION = "v3.0"
    MAX_RECORDS = 10000
    CHUNK_SIZE = 10

    EMPTY_RESPONSE = (
        "Não há informação disponível no sistema para gerar este relatório."
    )

    def __init__(self, model: ChatOllama):
        self.model = model

        self.system_prompt = SystemMessage(
            content=self._build_system_prompt()
        )

    # --------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------

    def _build_system_prompt(self) -> str:
        return f"""
Você é responsável por gerar blocos de registros de relatórios OFICIAIS do sistema Gestock.

VERSÃO DO PROMPT: {self.PROMPT_VERSION}

REGRAS ABSOLUTAS:

1. Utilize EXCLUSIVAMENTE os dados recebidos
2. Nunca gere título do relatório
3. Nunca gere totais
4. Nunca gere parâmetros
5. Gere APENAS os registros formatados
6. Nunca interprete dados
7. Nunca invente informações
""".strip()

    # --------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------

    def _get_prompt(self, report_type: str) -> str:
        prompt = PROMPTS.get(report_type)

        if not prompt:
            raise ValueError(f"Prompt não encontrado para {report_type}")

        return prompt

    # --------------------------------------------------
    # EXECUÇÃO PRINCIPAL
    # --------------------------------------------------

    async def gerar(self, report_input: ReportInput):

        registros = (
            report_input.dados.get("registros")
            or report_input.dados.get("data")
            or []
        )

        metadata = report_input.dados.get("metadata") or {}

        if not registros:
            return self.EMPTY_RESPONSE

        if len(registros) > self.MAX_RECORDS:
            registros = registros[:self.MAX_RECORDS]
            metadata["limite_aplicado"] = self.MAX_RECORDS

        return await self.generate_report(
            report_type=report_input.report_type,
            dados=registros,
            parametros=report_input.parametros or {},
            metadata=metadata
        )

    # --------------------------------------------------
    # CHUNK LLM CALL
    # --------------------------------------------------

    async def _gerar_chunk(
        self,
        prompt_template: str,
        chunk: list,
        parametros: dict,
        metadata: dict | None
    ) -> str:

        prompt = prompt_template.format(
            dados=json.dumps(chunk, ensure_ascii=False, indent=2),
            parametros=parametros,
            metadata=metadata or {},
            total_items=len(chunk)
        )

        messages = [
            self.system_prompt,
            HumanMessage(content=prompt)
        ]

        response = await self.model.ainvoke(messages)

        return response.content.strip()

    # --------------------------------------------------
    # GERAÇÃO COMPLETA
    # --------------------------------------------------

    async def generate_report(
        self,
        report_type: str,
        dados: list,
        parametros: dict,
        metadata: dict | None = None
    ):

        formatter = FORMATTERS.get(report_type)

        if not formatter:
            raise ValueError(f"Formatter não encontrado para {report_type}")

        prompt_template = self._get_prompt(report_type)

        # divide dados em chunks
        chunks = [
            dados[i:i + self.CHUNK_SIZE]
            for i in range(0, len(dados), self.CHUNK_SIZE)
        ]

        registros_formatados = []

        # chama LLM por chunk
        contador_global = 1

        for chunk in chunks:

            prompt = prompt_template.format(
                dados=chunk,
                parametros=parametros,
                metadata=metadata or {},
                total_items=len(dados),
                start_index=contador_global
            )

            messages = [
                self.system_prompt,
                HumanMessage(content=prompt)
            ]

            response = await self.model.ainvoke(messages)
            registros_formatados.append(response.content)

            contador_global += len(chunk)

        # monta relatório final via formatter
        relatorio_final = formatter.montar_relatorio(
            registros_formatados=registros_formatados,
            parametros=json.dumps(parametros, ensure_ascii=False, indent=2),
            total_items=len(dados),
            metadata=metadata
        )

        return relatorio_final
