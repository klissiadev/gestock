from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.movimentacao_service import MovimentacaoService

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


def get_service(conn=Depends(get_connection)):
    return MovimentacaoService(conn)


# -------- ENTRADA --------
@router.post("/entrada")
def registrar_entrada(dados: dict, service: MovimentacaoService = Depends(get_service)):
    return service.registrar_entrada(dados)


@router.get("/entrada")
def listar_entradas(service: MovimentacaoService = Depends(get_service)):
    return service.listar_entradas()


# -------- SAÍDA --------
@router.post("/saida")
def registrar_saida(dados: dict, service: MovimentacaoService = Depends(get_service)):
    return service.registrar_saida(dados)


@router.get("/saida")
def listar_saidas(service: MovimentacaoService = Depends(get_service)):
    return service.listar_saidas()