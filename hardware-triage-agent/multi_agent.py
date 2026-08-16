import os
import json
from typing import TypedDict
import google.generativeai as genai
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Importamos a função de triagem do módulo agent.py
from agent import run_triage_agent

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ==========================================
# 1. NOVO SCHEMA PARA O AGENTE REVISOR
# ==========================================
class RelatorioQA(BaseModel):
    analise_de_risco_legal: str = Field(
        description="Análise detalhada se o e-mail redigido pelo suporte admite culpa indevida ou gera passivo jurídico."
    )
    precisou_ajustes: bool = Field(
        description="True se o e-mail original violava regras e precisou ser alterado. False se estava perfeito."
    )
    email_final_aprovado: str = Field(
        description="O texto final do e-mail, já corrigido (se necessário), pronto para envio."
    )

# ==========================================
# 2. ATUALIZANDO O ESTADO DO GRAFO
# ==========================================
class AgentState(TypedDict):
    ticket_original: str
    diagnostico_json: str
    email_resposta_rascunho: str # Mudamos o nome para rascunho
    relatorio_qa_json: str       # O JSON final do Agente de Compliance

# ==========================================
# 3. OS NÓS (AGENTES)
# ==========================================

# NÓ 1: Agente Triador
def agente_triagem(state: AgentState):
    print("🤖 [Agente 1 - Triagem] Extraindo dados técnicos do ticket...")
    resultado_json = run_triage_agent(state["ticket_original"])
    return {"diagnostico_json": resultado_json}

# NÓ 2: Agente Redator
def agente_redator(state: AgentState):
    print("✍️  [Agente 2 - Redator] Escrevendo a primeira versão do e-mail...")
    dados = json.loads(state["diagnostico_json"])
    
    system_prompt = """
    Você é o Especialista de Comunicação. Redija um e-mail de resposta direta ao cliente.
    Seja muito empático e detalhe as falhas técnicas (Xeon não tem vídeo e fonte é fraca).
    """
    
    prompt_final = f"Ticket:\n{state['ticket_original']}\n\nLaudo:\n{json.dumps(dados)}\n\nEscreva o e-mail:"
    model = genai.GenerativeModel(model_name="models/gemini-3.5-flash", system_instruction=system_prompt)
    response = model.generate_content(prompt_final, generation_config=genai.GenerationConfig(temperature=0.7))
    
    return {"email_resposta_rascunho": response.text}

# NÓ 3: Agente de Compliance (NOVO!)
def agente_compliance(state: AgentState):
    print("🔎 [Agente 3 - Compliance] Auditando riscos legais no rascunho (LLM-as-a-Judge)...")
    
    system_prompt = """
    Você é o Advogado Chefe de Compliance da empresa.
    Sua missão é auditar o e-mail de suporte antes do envio ao cliente.
    
    REGRAS INEGOCIÁVEIS:
    1. A empresa NUNCA deve pedir desculpas pela ignorância técnica do cliente na compra de peças avulsas.
    2. Não admita falha nos nossos produtos, foque na incompatibilidade do projeto do cliente.
    3. Mantenha um tom profissional, mas firme.
    
    Se o e-mail do Redator violar essas regras, aplique as devidas correções e gere a versão final segura.
    """
    
    prompt_final = f"Ticket Original:\n{state['ticket_original']}\n\nRascunho do E-mail gerado pelo Suporte:\n{state['email_resposta_rascunho']}\n\nFaça a auditoria e preencha o relatório:"
    
    model = genai.GenerativeModel(model_name="models/gemini-3.5-flash", system_instruction=system_prompt)
    
    response = model.generate_content(
        prompt_final,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=RelatorioQA,
            temperature=0.1 # Temperatura baixa pois é uma auditoria rigorosa
        )
    )
    
    return {"relatorio_qa_json": response.text}

# ==========================================
# 4. ORQUESTRANDO O GRAFO COM 3 AGENTES
# ==========================================
workflow = StateGraph(AgentState)

workflow.add_node("triador", agente_triagem)
workflow.add_node("redator", agente_redator)
workflow.add_node("auditor", agente_compliance)

workflow.set_entry_point("triador")
# A linha de montagem agora tem mais um passo:
workflow.add_edge("triador", "redator")
workflow.add_edge("redator", "auditor")
workflow.add_edge("auditor", END)

app = workflow.compile()

# ==========================================
# TESTANDO A INTEGRAÇÃO
# ==========================================
if __name__ == "__main__":
    
    ticket_cliente = """
    Comprei as peças com vocês mês passado para montar um servidor caseiro. 
    Coloquei um processador Xeon E3-1270 V2 numa placa-mãe H61 que eu já tinha. O PC liga os coolers, 
    mas dá tela preta direto, não bipa e não dá vídeo de jeito nenhum. A minha fonte é uma genérica 
    de 200W. Quero abrir um processo de devolução no juizado especial se vocês não trocarem a placa.
    """
    
    print("Iniciando Pipeline Avançado de Inteligência Artificial...\n")
    print("-" * 60)
    
    estado_final = app.invoke({"ticket_original": ticket_cliente})
    
    print("-" * 60)
    
    # Processando o JSON final do auditor
    relatorio = json.loads(estado_final["relatorio_qa_json"])
    
    print("\n📋 RELATÓRIO INTERNO DE AUDITORIA (COMPLIANCE):")
    print(f"Risco Legal Apontado: {relatorio['analise_de_risco_legal']}")
    print(f"Houve necessidade de ajuste jurídico no e-mail? {'SIM' if relatorio['precisou_ajustes'] else 'NÃO'}")
    
    print("\n" + "=" * 60)
    print("📩 E-MAIL FINAL APROVADO PARA ENVIO:")
    print("=" * 60 + "\n")
    print(relatorio['email_final_aprovado'])