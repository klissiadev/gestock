from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.movimentacao_service import MovimentacaoService

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


def get_service(conn=Depends(get_connection)):
    return MovimentacaoService(conn)


@router.post("/")
def registrar_movimentacao(movimentacao: dict, service: MovimentacaoService = Depends(get_service)):
    return service.registrar_movimentacao(movimentacao)


@router.get("/")
def listar_movimentacoes(service: MovimentacaoService = Depends(get_service)):
    return service.listar_movimentacoes()
