import pytest_asyncio
import pytest
import json
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
    
    # Executa a chamada
    mensagens = await bot.send_message(pergunta)
    resposta = mensagens[-1].content.lower()
    print(resposta)

    if caso.get('should_answer') is False:
        termos_recusa = ["não encontrei", "não tenho informação", "não existe", "desculpe", "lamento"]
        
        if caso.get('expected_behavior') == "ask_for_clarification":
            termos_recusa.extend(["qual", "especifique", "refere-se", "mais detalhes"])
            
        assert any(termo in resposta for termo in termos_recusa), \
            f"FALHA [{id_teste}]: A LLM deveria ter recusado ou pedido clarificação, mas respondeu: {resposta}"

    else:
        if 'expected_value' in caso:
            valor_esperado = str(caso['expected_value'])
            assert valor_esperado in resposta, \
                f"FALHA [{id_teste}]: Valor {valor_esperado} não encontrado na resposta."

        if 'expected_entities' in caso:
            for entidade in caso['expected_entities']:
                assert entidade.lower() in resposta, \
                    f"FALHA [{id_teste}]: Entidade '{entidade}' ausente na resposta."

        if 'expected_result' in caso:
            assert caso['expected_result'].lower() in resposta, \
                f"FALHA [{id_teste}]: Esperava-se o resultado '{caso['expected_result']}'."