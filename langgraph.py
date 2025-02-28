from dotenv import load_dotenv
import os
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

# Carrega variáveis do ambiente
load_dotenv()
chave_api = os.getenv("OPENAI_KEY")  

if chave_api is None:  
    print("Erro ao carregar chave da API")  

# Função para validar se a pergunta é matemática
def validar_pergunta(pergunta):
    padrao = r"[0-9+\-*/]"  
    return re.match(padrao, pergunta)  

# Nó do Receptor
def receptor(state):
    pergunta = state["pergunta"]
    if validar_pergunta(pergunta):  
        return {"pergunta": pergunta, "categoria": "matematica"}
    else:
        return {"erro": "A pergunta precisa ser matemática."}

# Nó do Professor Virtual
def professor_virtual(state):
    if "erro" in state:
        return state  

    modelo = ChatOpenAI(model="gpt-3.5", openai_api_key=chave_api)  
    
    mensagens = [
        SystemMessage(content="Responda a questão matemática:"),
        HumanMessage(content=state["pergunta"])
    ]
    
    resposta = modelo.invoke(mensagens).content  

    return {"pergunta": state["pergunta"], "resposta": resposta}

# Criando o grafo
grafo = StateGraph()  

grafo.add_node("receptor", receptor)
grafo.add_node("professor", professor_virtual)

# Definir transições entre os nós
grafo.set_entry_point("receptor")
grafo.add_edge("receptor", "professor")
grafo.add_edge("professor", "fim")  

# Compilar o fluxo
fluxo = grafo.compile()

# Executando o grafo com uma entrada
entrada_usuario = {"pergunta": "Qual é a raiz quadrada de 16?"}
resultado = fluxo.invoke(entrada_usuario)  

# Exibir a resposta final
print(json.dumps(resultado, indent=2, ensure_ascii=False))
