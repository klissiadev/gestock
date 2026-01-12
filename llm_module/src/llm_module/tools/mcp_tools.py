from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import tool

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
    Retorna a data e hora atual.
    """
    mcp_tool = await _get_mcp_time_tool()
    result = await mcp_tool.ainvoke({"timezone": "America/Manaus"})
    
    # Formatando a saida
    texto_json = result[0]["text"]
    import json
    dados = json.loads(texto_json)
    
    return json.dumps(dados, ensure_ascii=False, indent=2)

