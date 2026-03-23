from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from typing import Annotated

from request_module.models.RequestModel import RequestModel
from request_module.utils import mail_sender

from auth_module.models.User import UserPublic
from auth_module.utils.security import get_current_user
from backend.database.base import get_db
from backend.services.event_service import EventService
from backend.database.schemas import NotificationEventCreate

router = APIRouter(prefix="/requisicoes", tags=["Requisições"])
@router.post("/", status_code=201)
async def criar_requisicao(
    request: Request, 
    payload: RequestModel, 
    background_tasks: BackgroundTasks,
    user: Annotated[UserPublic, Depends(get_current_user)],
    db = Depends(get_db) 
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

                # inserir itens
                for item in payload.itens:
                    await conn.execute(
                        """
                        INSERT INTO app_core.itens_requisicoes 
                        (requisicao_id, produto_id, quantidade, prioridade)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (requisicao_id, item.produto_id, item.quantidade, item.prioridade)
                    )

            total_itens = len(payload.itens)

            event_service = EventService(db)

            event = NotificationEventCreate(
                type="SUCCESS",
                context={
                    "state": "REQUEST_SUCCESS",
                    "data": {
                        "titulo": payload.titulo,
                        "qty": total_itens
                    }
                },
                reference={
                    "id": requisicao_id,
                    "type": "REQUEST"
                }
            )

            event_service.criar_evento(event, user.id)

            nomes_map = await mail_sender.buscar_nomes_produtos(pool, payload.itens)

            dados_email = payload.model_dump()
            dados_email['id_banco'] = requisicao_id

            for item in dados_email['itens']:
                item['nome_produto'] = nomes_map.get(
                    item['produto_id'], 
                    "Produto não encontrado"
                )

            background_tasks.add_task(
                mail_sender.workflow_envio_email,
                dados_email
            )
            
            return {
                "status": "success",
                "id": requisicao_id
            }

        except Exception as e:
            print(f"Erro ao salvar requisição: {e}")
            raise HTTPException(
                status_code=500, 
                detail="Erro ao processar requisição no banco."
            )