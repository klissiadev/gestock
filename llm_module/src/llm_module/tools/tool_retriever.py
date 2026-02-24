from langchain_ollama import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from llm_module.tools.sql_tools import MINERVA_SQL_TOOLS

# APLICAÇÃO DE RAG NAS TOOLS DA MINERVA
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def _configurar_banco_vetorial():
    """
    Transforma as descrições das suas ferramentas em vetores usando o Ollama.
    """
    documentos_das_tools = []
    
    for ferramenta in MINERVA_SQL_TOOLS:
        doc = Document(
            page_content=ferramenta.description, 
            metadata={"nome_tool": ferramenta.name}
        )
        documentos_das_tools.append(doc)
    
    print(f"Gerando embeddings no Ollama para {len(MINERVA_SQL_TOOLS)} tools...")
    vector_store = FAISS.from_documents(documentos_das_tools, embeddings)
    print("Banco vetorial de tools pronto!")
    
    return vector_store


TOOL_VECTOR_STORE = _configurar_banco_vetorial()

def recuperar_tools_relevantes(pergunta_usuario: str, limite: int = 5) -> list:
    """Retorna apenas os objetos Tool mais relevantes para a pergunta"""
    docs_recuperados = TOOL_VECTOR_STORE.similarity_search(pergunta_usuario, k=limite)
    nomes_encontrados = [doc.metadata["nome_tool"] for doc in docs_recuperados]
    
    return [t for t in MINERVA_SQL_TOOLS if t.name in nomes_encontrados]