from fastapi import APIRouter, Depends, Response
from typing import List
import io
import pandas as pd
from backend.services.views_service import view_service
from backend.database.base import get_db
from backend.models.product_filters import product_filters
from backend.models.transaction_filters import transaction_filters
from backend.models.product_item import ProductSchema, ExportProduct
from backend.models.transaction_schema import TransactionSchema
from datetime import datetime
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from backend.utils.export_helper import generate_excel_report

router = APIRouter(prefix="/views", tags=["visualizar"])

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
    
    # Formatando
    dado_formatado = [ExportProduct.model_validate(item).model_dump() for item in dado_bruto]
    df = pd.DataFrame(dado_formatado)
    coluna_presentes = [col for col in PRODUCT_HEADERS.keys() if col in df.columns]
    df = df[coluna_presentes]
    df = df.rename(columns=PRODUCT_HEADERS)
    
    excel_content = generate_excel_report(
        df=df,
        title="Relatório Geral de Produtos em Estoque",
        sheet_name="Produtos"
    )

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
    
    dado_bruto = view.see_transaction_table(
        direcao=direcao, 
        order_by=filter.orderBy, 
        search_term=filter.searchTerm
    )
    
    # Formatando
    dado_formatado = [TransactionSchema.model_validate(item).model_dump() for item in dado_bruto]
    df = pd.DataFrame(dado_formatado)
    coluna_presentes = [col for col in MOVIMENTACAO_HEADERS.keys() if col in df.columns]
    df = df[coluna_presentes]
    df = df.rename(columns=MOVIMENTACAO_HEADERS)
    
    excel_content = generate_excel_report(
        df=df,
        title="Relatório Geral de Movimentação em Estoque",
        sheet_name="Movimentações"
    )

    filename = f"movimentacoes_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
    
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )