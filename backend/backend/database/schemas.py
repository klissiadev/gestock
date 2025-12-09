PRODUCT_SCHEMA = {
    "table": "produtos",
    "columns": {
        "nome": {"type": "str", "required": True},
        "preco": {"type": "float", "required": True},
        "quantidade": {"type": "int", "required": True},
    }
}

# Vamos adicionar mais schemas aqui:
# CLIENT_SCHEMA = {...}
# ESTOQUE_SCHEMA = {...}

IMPORT_SCHEMAS = {
    "produtos": PRODUCT_SCHEMA
}