from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


# =========================
# Schemas
# =========================

class ReportInput(BaseModel):
    """
    Estrutura oficial de entrada para geração de relatórios.
    """
    tipo: str = Field(..., description="Tipo do relatório (ex: estoque, movimentações, auditoria)")
    dados: Any = Field(..., description="Dados consolidados para geração do relatório")
    parametros: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Parâmetros adicionais usados no relatório"
    )


# =========================
# Agent
# =========================

class ReportAgent:
    """
    Agente especializado exclusivamente em geração de relatórios oficiais.
    Não possui memória, não usa ferramentas e não consulta banco de dados.
    """

    PROMPT_VERSION = "v1.0"

    def __init__(self, model: ChatOllama):
        self.model = model
        self.system_prompt = SystemMessage(content=self._build_system_prompt())

    def _build_system_prompt(self) -> str:
        return f"""
Você é um agente especializado em geração de relatórios oficiais do sistema Gestock.

VERSÃO DO PROMPT: {self.PROMPT_VERSION}

REGRAS ABSOLUTAS:
- Você NÃO consulta banco de dados.
- Você NÃO inventa informações.
- Você NÃO faz suposições ou estimativas.
- Você utiliza APENAS os dados fornecidos na entrada.
- Se algum dado estiver ausente, deixe isso explicitamente claro no relatório.
- Você NÃO faz perguntas ao usuário.
- Você NÃO menciona ferramentas, modelos ou processos internos.
- O texto gerado é o RELATÓRIO FINAL do sistema.

ESTILO:
- Linguagem clara, objetiva e profissional.
- Estrutura lógica e bem organizada.
- Adequado para uso institucional e auditoria.
""".strip()

    def _build_user_prompt(self, report: ReportInput) -> str:
        return f"""
TIPO DE RELATÓRIO:
{report.tipo}

PARÂMETROS:
{report.parametros}

DADOS:
{report.dados}

Gere o relatório correspondente seguindo rigorosamente as regras definidas.
""".strip()

    async def gerar(self, report_input: ReportInput) -> str:
        """
        Gera o relatório final baseado exclusivamente nos dados fornecidos.
        """
        response = await self.model.ainvoke([
            self.system_prompt,
            HumanMessage(content=self._build_user_prompt(report_input))
        ])

        return response.content
