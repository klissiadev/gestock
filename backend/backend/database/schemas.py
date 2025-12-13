PRODUTO_SCHEMA = {
    "table": "Produto",
    "columns": {
        "nome": {
            "type": "str",
            "required": True
        },
        "descricao": {
            "type": "str",
            "required": False
        },
        "categoria": {
            "type": "str",
            "required": True
        },
        "estoque_atual": {
            "type": "int",
            "required": True
        },
        "estoque_minimo": {
            "type": "int",
            "required": True
        },
        "data_cadastro": {
            "type": "date",
            "required": True
        },
        "data_validade": {
            "type": "date",
            "required": False
        },
        "valor_unitario": {
            "type": "float",
            "required": True
        }
    }
}

MOVIMENTACAO_SCHEMA = {
    "table": "Movimentacao",
    "columns": {
        "tipo_movimento": {
            "type": "str",
            "required": True
        },
        "data_movimento": {
            "type": "date",
            "required": True
        },
        "quantidade": {
            "type": "int",
            "required": True
        },
        "observacao": {
            "type": "str",
            "required": False
        },
        "id_usuario": {
            "type": "int",
            "required": True
        },
        "cod_produto": {
            "type": "int",
            "required": True
        }
    }
}

IMPORT_SCHEMAS = {
    "Produto": PRODUTO_SCHEMA,
    "Movimentacao": MOVIMENTACAO_SCHEMA
}