from langchain.agents.middleware import (
    ModelCallLimitMiddleware, 
    ContextEditingMiddleware, 
    ClearToolUsesEdit,
)

limitador_chamadas = ModelCallLimitMiddleware(
    run_limit=5,
    thread_limit=None,
    exit_behavior="end"
)

editor_contexto = ContextEditingMiddleware(
    edits=[
        ClearToolUsesEdit(
            trigger=6000,
            keep=2,
            clear_tool_inputs=False,
            placeholder="[Resultados antigos da ferramenta removidos para liberar memória]"
        ),
        
    ],
    token_count_method="approximate"
)


