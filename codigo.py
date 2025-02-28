from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import json
import re

def validar_pergunta(pergunta):
    # Verifica se a pergunta contém caracteres matemáticos básicos
    padrao = r"[0-9+\-*/=x]"
    return bool(re.search(padrao, pergunta))

def processar_pergunta(pergunta):
    if not validar_pergunta(pergunta):
        return {"erro": "A pergunta não parece ser matemática."}
    
    # Criando o JSON de entrada
    entrada_json = {
        "pergunta": pergunta,
        "categoria": "matemática"
    }
    
    return entrada_json

def professor_virtual(entrada_json):
    """
    Simula a resposta de um "Professor Virtual" usando LangChain.
    """
    load_dotenv()
    chave_api = os.getenv("OPENAI_API_KEY")
    
    if not chave_api:
        return {"erro": "Chave da API OpenAI não configurada."}
    
    modelo = ChatOpenAI(model="gpt-3.5-turbo", api_key=chave_api)
    
    mensagens = [
        SystemMessage("Responda a pergunta matemática a seguir."),
        HumanMessage(entrada_json["pergunta"])
    ]
    
    resposta = modelo.invoke(mensagens)
    
    return {"resposta": resposta}


# Teste do sistema
pergunta = "Resolva a equação 2x + 3 = 7"
entrada_json = processar_pergunta(pergunta)
if "erro" not in entrada_json:
    resposta = professor_virtual(entrada_json)
    print(json.dumps(resposta, indent=2, ensure_ascii=False))
else:
    print(json.dumps(entrada_json, indent=2, ensure_ascii=False))
