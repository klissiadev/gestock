class AnalysisBuilder:

    @staticmethod
    def resumo_movimentacao(registros):

        total_entradas = 0
        total_saidas = 0

        for item in registros:
            if item["tipo_movimentacao"] == "entrada":
                total_entradas += item["quantidade"]
            else:
                total_saidas += item["quantidade"]

        return {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": total_entradas - total_saidas,
            "total_registros": len(registros)
        }
    
    
    @staticmethod
    def total_por_produto(registros):

        resultado = {}

        for item in registros:
            produto = item["nome_produto"]

            resultado.setdefault(produto, 0)
            resultado[produto] += item["quantidade"]

        return resultado
    

    @staticmethod
    def total_por_tipo(registros):

        resultado = {"entrada": 0, "saida": 0}

        for item in registros:
            resultado[item["tipo_movimentacao"]] += item["quantidade"]

        return resultado