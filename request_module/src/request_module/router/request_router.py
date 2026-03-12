from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from typing import Annotated

from request_module.models.RequestModel import RequestModel, RequestItem
from request_module.utils import mail_sender
from auth_module.models.User import UserPublic
from auth_module.utils.security import get_current_user

router = APIRouter(prefix="/requisicoes", tags=["Requisições"])

@router.post("/", status_code=201)
async def criar_requisicao(
    request: Request, 
    payload: RequestModel, 
    background_tasks: BackgroundTasks,
    user: Annotated[UserPublic, Depends(get_current_user)]
):
    pool = request.app.state.db_pool
    
    async with pool.connection() as conn:
        try:
            async with conn.transaction():
                cursor = await conn.execute(
                    """
                    INSERT INTO app_core.requisicoes (titulo, observacao, user_id)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (payload.titulo, payload.observacao, user.id)
                )
                res = await cursor.fetchone()
                requisicao_id = res['id']


                for item in payload.itens:
                    await conn.execute(
                        """
                        INSERT INTO app_core.itens_requisicoes 
                        (requisicao_id, produto_id, quantidade, prioridade)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (requisicao_id, item.produto_id, item.quantidade, item.prioridade)
                    )

            # --- Fora da transação de inserir ---
    
            # 3. Buscar nomes dos produtos para o e-mail
            nomes_map = await mail_sender.buscar_nomes_produtos(pool, payload.itens)

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