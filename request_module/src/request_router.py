from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from .schemas import RequestModel # Ajuste o import conforme sua pasta
from .utils import mail_sender, db_utils

router = APIRouter(prefix="/requisicoes", tags=["Requisições"])

@router.post("/", status_code=201)
async def criar_requisicao(
    request: Request, 
    payload: RequestModel, 
    background_tasks: BackgroundTasks
):
    pool = request.app.state.db_pool
    
    async with pool.connection() as conn:
        try:
            # Iniciamos uma transação atômica
            async with conn.transaction():
                # 1. Inserir o Cabeçalho
                cursor = await conn.execute(
                    """
                    INSERT INTO app_core.requisicoes (titulo, descricao, motivo, prioridade)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (payload.titulo, payload.descricao, payload.motivo, payload.prioridade)
                )
                res = await cursor.fetchone()
                requisicao_id = res['id']

                # 2. Inserir os Itens
                for item in payload.itens:
                    await conn.execute(
                        """
                        INSERT INTO app_core.itens_requisicoes 
                        (requisicao_id, produto_id, quantidade, observacao)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (requisicao_id, item.produto_id, item.quantidade, item.observacao)
                    )

            # --- Fora da transação (após o commit automático) ---

            # 3. Buscar nomes dos produtos para o e-mail (UX do Financeiro)
            nomes_map = await db_utils.buscar_nomes_produtos(pool, payload.itens)

            # 4. Preparar dados para a tarefa de fundo
            dados_email = payload.model_dump()
            dados_email['id_banco'] = requisicao_id
            for item in dados_email['itens']:
                item['nome_produto'] = nomes_map.get(item['produto_id'], "Produto não encontrado")

            # 5. Disparar e-mail em segundo plano
            background_tasks.add_task(mail_sender.workflow_envio_email, dados_email)
            
            return {"status": "success", "id": requisicao_id}

        except Exception as e:
            print(f"Erro ao salvar requisição: {e}")
            raise HTTPException(status_code=500, detail="Erro ao processar requisição no banco.")