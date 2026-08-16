from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Importa o pipeline de agentes que já construímos!
from multi_agent import app as agent_workflow

# 1. Instancia o servidor FastAPI
api = FastAPI(
    title="HardwareTech Triage API",
    description="API Corporativa Multi-Agente para Triagem de Suporte Técnico",
    version="1.0.0"
)

# 2. Define o Schema de Entrada (O que o cliente/sistema vai enviar para a API)
class TicketRequest(BaseModel):
    ticket_text: str

# 3. Define o Schema de Saída (O que a API vai devolver para o sistema)
class APIResponse(BaseModel):
    risco_legal_identificado: str
    email_auditado_para_envio: str
    status: str = "sucesso"

# 4. A Rota POST
@api.post("/api/v1/triage", response_model=APIResponse)
async def processar_ticket(request: TicketRequest):
    """
    Recebe um ticket de texto bruto e aciona o pipeline de 3 agentes
    (Triador -> Redator -> Compliance) para gerar a resposta final.
    """
    try:
        # Aciona o LangGraph passando o texto recebido na requisição web
        estado_final = agent_workflow.invoke({"ticket_original": request.ticket_text})
        
        # Puxa o JSON final gerado pelo último agente (Agente de Compliance)
        relatorio_qa = json.loads(estado_final["relatorio_qa_json"])
        
        # Devolve a resposta limpa e estruturada para quem chamou a API
        return APIResponse(
            risco_legal_identificado=relatorio_qa["analise_de_risco_legal"],
            email_auditado_para_envio=relatorio_qa["email_final_aprovado"]
        )
        
    except Exception as e:
        # Tratamento de erro padrão de API
        raise HTTPException(status_code=500, detail=f"Erro interno nos agentes: {str(e)}")