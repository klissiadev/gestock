import pytest_asyncio
import pytest
import json
import re, unicodedata
from llm_module.models.chatbot import chat_bot_service

def carregar_testes():
    with open('test_cases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    casos = []
    for categoria, itens in data.items():
        for item in itens:
            if 'paraphrases' in item:
                for p in item['paraphrases']:
                    casos.append({**item, "question": p, "categoria": categoria})
            else:
                casos.append({**item, "categoria": categoria})
    return casos

def remove_acentos(s):
    return "".join(
        c for c in unicodedata.normalize("NFKD", s.lower())
        if not unicodedata.combining(c)
    )

@pytest_asyncio.fixture
async def bot():
    """Instancia o chatbot uma vez para os testes"""
    return chat_bot_service()

# --- TESTE PRINCIPAL PARAMETRIZADO ---
@pytest.mark.asyncio
@pytest.mark.parametrize("caso", carregar_testes())
async def test_llm_behavior(bot, caso):
    pergunta = caso['question']
    id_teste = caso['id']
    
    mensagens = await bot.send_message(pergunta)
    resposta = mensagens[-1].content.lower()
    
    # Imprime todas as respostas, aprovadas ou não
    print(f"\n[{id_teste}] Pergunta: {pergunta}")
    print(f"[{id_teste}] Resposta LLM: {mensagens}\n")

    # --- CASO A LLM N DEVA RESPONDER ---
    if caso.get('should_answer') is False:
        termos_recusa = [
            "não encontrei", "não tenho informação", "não existe",
            "desculpe", "lamento", "não há informações", "infelizmente",
            "não podemos", "não é possível", "não há dados", "sem dados", 
            "não disponível", "não posso determinar", "não conseguimos estimar",
            "não temos dados", "não é possível responder", "não temos informação suficiente",
            "não estão disponíveis", "não podemos", "sem dados", "não há informação", "não possuo", "não está disponível"
        ]
        
        if caso.get('expected_behavior') == "ask_for_clarification":
            termos_recusa.extend([
                "qual", "especifique", "refere-se", "mais detalhes", "ter mais detalhes"
            ])
        # Testa se pelo menos um termo aparece
        assert any(termo in resposta for termo in termos_recusa), \
            f"FALHA [{id_teste}]: A LLM deveria ter recusado ou pedido clarificação, mas respondeu: {resposta}"

    # --- CASO A LLM DEVA RESPONDER ---
    else:
        # 1️⃣ Checa valores exatos
        if 'expected_value' in caso:
            valor_esperado = str(caso['expected_value'])
            assert valor_esperado in resposta, \
                f"FALHA [{id_teste}]: Valor {valor_esperado} não encontrado na resposta."


        # 2️⃣ Checa entidades esperadas
        if 'expected_entities' in caso:
            for entidade in caso['expected_entities']:
                assert remove_acentos(entidade.lower()) in remove_acentos(resposta), \
                    f"FALHA [{id_teste}]: Entidade '{entidade}' ausente na resposta."

        # 3️⃣ Checa resultados esperados de comportamento específico
        if 'expected_result' in caso:
            assert caso['expected_result'].lower() in resposta, \
                f"FALHA [{id_teste}]: Esperava-se o resultado '{caso['expected_result']}'."
