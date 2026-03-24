from llm_module.models.intent_classifier import IntentClassifier
from llm_module.services.llm_service import LLMService as GeneralLLMService
from llm_report.services.llm_service import LLMService as ReportLLMService
from llm_module.audit.logger import AuditLogger # Importe o logger
import asyncio

class MinervaGateway:
    def __init__(self, connection_pool):
        self.intent_classifier = IntentClassifier() # Corrigido o nome da classe
        self.general_service = GeneralLLMService(connection_pool)
        self.report_service = ReportLLMService() 
        self.audit = AuditLogger(connection_pool) # Gateway passa a ser responsável pelo log
        self._background_tasks = set()
        
    async def ensure_init(self):
        await self.general_service.ensure_init()
        await self.report_service._ensure_init()

    async def send_message(self, message: str, session_id: str):
        await self.ensure_init()
        
        intent = await self.intent_classifier.classify_intent(message)
        print(f"Intenção detectada pelo Gateway: {intent}")
        
        if intent == "RELATORIO":
            resposta = await self.report_service.send_message(message, session_id)
        else:
            resposta = await self.general_service.send_message(message, session_id)
            
        # Salva a auditoria idependente de qual LLM respondeu
        self._background_tasks.add(asyncio.create_task(
            self.audit.save_conversation(session_id, message, resposta)
        ))
        return resposta

    async def stream_message(self, message: str, session_id: str):
        await self.ensure_init()
        
        intent = await self.intent_classifier.classify_intent(message)
        print(f"Intenção detectada pelo Gateway (Stream): {intent}")
        
        full_response = []
        
        if intent == "RELATORIO":
            async for chunk in self.report_service.stream_message(message, session_id):
                if chunk: full_response.append(chunk)
                yield chunk
        else:
            async for chunk in self.general_service.stream_message(message, session_id):
                if chunk: full_response.append(chunk)
                yield chunk
                
        # Salva o texto completo no final do stream
        complete_text = "".join(full_response)
        self._background_tasks.add(asyncio.create_task(
            self.audit.save_conversation(session_id, message, complete_text)
        ))
        
    async def close(self):
        await self.general_service.close()
        