from fastapi import APIRouter, Depends
from backend.database.base import get_connection
from backend.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def get_service(conn=Depends(get_connection)):
    return ProdutoService(conn)


@router.post("/")
def criar_produto(produto: dict, service: ProdutoService = Depends(get_service)):
    return service.criar_produto(produto)


@router.get("/")
def listar_produtos(service: ProdutoService = Depends(get_service)):
    return service.listar_produtos()


@router.get("/{produto_id}/nome")
def buscar_produto(produto_id: int, service: ProdutoService = Depends(get_service)):
    return service.get_nome_produto(produto_id)
