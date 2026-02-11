class MovementBuilder:

    @staticmethod
    def agrupar_entradas_saidas(registros):

        agrupado = {}

        for item in registros:

            produto = item["nome_produto"]
            entidade = item["entidade"]
            quantidade = item["total_quantidade"]
            tipo = item["tipo_movimentacao"]

            if produto not in agrupado:
                agrupado[produto] = {
                    "nome_produto": produto,
                    "total_entradas": 0,
                    "total_saidas": 0,
                    "entradas": [],
                    "saidas": []
                }

            registro = {
                "entidade": entidade,
                "quantidade": quantidade
            }

            if tipo == "entrada":
                agrupado[produto]["entradas"].append(registro)
                agrupado[produto]["total_entradas"] += quantidade

            elif tipo == "saida":
                agrupado[produto]["saidas"].append(registro)
                agrupado[produto]["total_saidas"] += quantidade

        return sorted(
            agrupado.values(),
            key=lambda x: x["nome_produto"]
        )
