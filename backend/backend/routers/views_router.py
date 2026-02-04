from fastapi import APIRouter, Depends, Response
from typing import List
import io
from fpdf import FPDF
import pandas as pd
from backend.services.views_service import view_service
from backend.database.base import get_db
from backend.models.product_filters import product_filters
from backend.models.transaction_filters import transaction_filters
from backend.models.product_item import ProductSchema
from backend.models.transaction_schema import TransactionSchema
from datetime import datetime

router = APIRouter(prefix="/views", tags=["visualizar"])

def _criar_excel(df: pd.DataFrame):
    output = io.BytesIO()
    # Usamos o engine openpyxl para gerar arquivos .xlsx
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')
    
    # Volta o ponteiro do arquivo para o início para que o FastAPI consiga ler
    output.seek(0)
    return output.getvalue()
    


# Constantes
MOVIMENTACAO_HEADERS = {
    "unique_id": "ID",
    "produto_nome": "Nome de Produto",
    "quantidade": "Quantidade",
    "data_evento": "Data da movimentação",
    "valor_unitario": "Valor unitário",
    "parceiro_origem": "Local de Origem",
    "local_destino": "Local de Destino",
    "tipo_movimento": "Tipo de Movimentação",
    "created_at": "Registrado em",
}

PRODUCT_HEADERS = {
    "id": "ID",
    "nome": "Nome do Produto",
    "tipo": "Tipo",
    "descricao": "Descrição",
    "estoque_atual": "Estoque Atual",
    "estoque_minimo": "Estoque Mínimo",
    "baixo_estoque": "Estoque Baixo?",
    "vencido": "Vencido?",
    "data_validade": "Validade",
    "ativo": "Ativo?"
}


@router.post("/product", response_model=List[ProductSchema])
async def exibir_tabela_produto(filter: product_filters, db=Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)

    product_table = view.see_product_table(
        direcao=direcao,
        order_by=filter.orderBy,
        search_term=filter.searchTerm,
        tipo=filter.categoria,
        apenas_baixo_estoque=filter.isBaixoEstoque,
        apenas_vencidos=filter.isVencido
    )
    
    print(product_table)
    return product_table



@router.post(path="/moviment", response_model=List[TransactionSchema])
async def exibir_tabela_movimentacao(filter: transaction_filters, db = Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)
    
    transaction_table = view.see_transaction_table(
        direcao=direcao, 
        order_by=filter.orderBy, 
        search_term=filter.searchTerm
    )
    
    return transaction_table



@router.post("/download/product")
async def download_tabela_produtos(filter: product_filters, db=Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)

    dado_bruto = view.see_product_table(
        direcao=direcao,
        order_by=filter.orderBy,
        search_term=filter.searchTerm,
        tipo=filter.categoria,
        apenas_baixo_estoque=filter.isBaixoEstoque,
        apenas_vencidos=filter.isVencido
    )
    
    dado_formatado = [ProductSchema.model_validate(item).model_dump() for item in dado_bruto]
    df = pd.DataFrame(dado_formatado)
    
    # Formatando as colunas
    coluna_presentes = [col for col in PRODUCT_HEADERS.keys() if col in df.columns]
    df = df[coluna_presentes]
    
    df = df.rename(columns=MOVIMENTACAO_HEADERS)
    
    excel_content = _criar_excel(df)
    filename = f"estoque_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
    
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )



@router.post("/download/transaction")
async def download_tabela_movimentacao(filter: transaction_filters, db=Depends(get_db)):
    direcao = "ASC" if filter.isAsc else "DESC"
    
    view = view_service(db)
    
    dados_puro = view.see_transaction_table(
        direcao=direcao, 
        order_by=filter.orderBy, 
        search_term=filter.searchTerm
    )
    
    formatted_data = [TransactionSchema.model_validate(item).model_dump() for item in raw_data]
    
    return transaction_table