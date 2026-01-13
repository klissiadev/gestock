from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import tool
from datetime import datetime

_client = MultiServerMCPClient(
    {
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "mcp-server-time",
                "--local-timezone=America/Boa_Vista",
            ],
        }
    }
)

async def get_all_mcp_tools():
    """
    Retorna TODOS os tools expostos pelos MCPs registrados.
    """
    return await _client.get_tools()

async def _get_mcp_time_tool():
    tools = await get_all_mcp_tools()
    for t in tools:
        if t.name == "get_current_time":
            return t
    raise RuntimeError("get_current_time não encontrado no MCP time")

@tool
async def tool_get_current_time() -> str:
    """
    Retorna a data e hora atual em um formato estruturado para comparações temporais.
    Uso principal:
        - Verificar se um produto está vencido ou próximo da data de validade.
        - Calcular intervalos de dias entre a data atual e uma data futura ou passada.
    """
    mcp_tool = await _get_mcp_time_tool()
    result = await mcp_tool.ainvoke({"timezone": "America/Manaus"})
    
    # Formatando a saida
    texto_json = result[0]["text"]
    import json
    dados = json.loads(texto_json)
    return json.dumps(dados, ensure_ascii=False, indent=2)

@tool
def tool_calcular_validade(data_validade: str) -> dict:
    """
        Compara a data de validade (formato ISO) com data de hoje
        Retorna se está vencido e quantos dias faltam.
    """ 
    validade = datetime.fromisoformat(data_validade).date()
    atual = datetime.now().date()
    
    delta = (validade - atual).days
    info = {}
    
    if delta > 0:
        info = {
            "status": "válido",
            "data_validade": data_validade,
            "mensagem": f"Faltam {delta} dias para vencer.", 
        }
    else:
        # Usamos abs(delta) para não ficar "vencido há -10 dias"
        info = {
            "status": "vencido",
            "data_validade": data_validade,
            "mensagem": f"Produto vencido há {abs(delta)} dias" if delta < 0 else "Produto vence hoje."
        }
    
    return info
