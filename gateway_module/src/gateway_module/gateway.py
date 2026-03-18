# llm_module/src/llm_module/services/minerva_gateway.py
from gateway_module.intent import IntentRouterService


class MinervaGateway:
    def __init__(self, connection_pool):
        self.intent_router = IntentRouterService()
        # self.general_service = GeneralLLMService()
        # self.report_service = ReportLLMService() 
        
    async def ensure_init(self):
        # await self.general_service.ensure_init()
        # await self.report_service._ensure_init() 
        pass

    async def send_message(self, message: str, session_id: str):
        await self.ensure_init()
        
        # Descobre a intenção
        intent = await self.intent_router.classify_intent(message)
        print(f"Intenção detectada pelo Gateway: {intent}")
        
        # 2. Roteia para o módulo correto
        if intent == "RELATORIO":
            return await self.report_service.send_message(message, session_id)
        else:
            return await self.general_service.send_message(message, session_id)

    # Mesma coisa de cima, só que com o stream message
    async def stream_message(self, message: str, session_id: str):
        await self.ensure_init()
        
        intent = await self.intent_router.classify_intent(message)
        print(f"Intenção detectada pelo Gateway (Stream): {intent}")
        
        if intent == "RELATORIO":
            async for chunk in self.report_service.stream_message(message, session_id):
                yield chunk
        else:
            async for chunk in self.general_service.stream_message(message, session_id):
                yield chunk