import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from models import TriageResponse

# 1. Carrega as variáveis e configura a API
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def run_triage_agent(customer_ticket: str) -> str:
    """
    Executa o agente de triagem utilizando a validação NATIVA do Gemini com Pydantic.
    """
    
    system_prompt = """
    Você é um Engenheiro de Triagem Nível 3 atuando em uma fabricante de tecnologia de alto desempenho.
    Sua função é analisar tickets de suporte técnico de clientes, diagnosticar a provável causa raiz e estruturar um plano de ação.

    DIRETIVAS DE DIAGNÓSTICO:
    1. Analise cuidadosamente os sintomas descritos.
    2. Identifique gargalos ou incompatibilidades (ex: processador Xeon sem vídeo integrado necessita de GPU dedicada, caso contrário gera tela preta).
    3. Problemas de energia ou desligamento geralmente apontam para falha na Fonte (PSU).

    REGRAS DE ROTEAMENTO (Assignee):
    - Ameaça de processo no juizado especial, Procon ou devolução -> "Legal"
    - Problemas de compatibilidade de peças -> "L2_Engineering"
    - Dúvidas de instalação básica -> "L1_Support"
    """

    # 2. Inicializa o modelo puramente com o SDK do Google
    model = genai.GenerativeModel(
        model_name="models/gemini-3.5-flash",
        system_instruction=system_prompt
    )

    # 3. Chama a API forçando a saída para o formato do Pydantic no GenerationConfig
    response = model.generate_content(
        f"Ticket do Cliente: {customer_ticket}",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=TriageResponse,
            temperature=0.1
        )
    )
    
    return response.text

# ==========================================
# TESTANDO O AGENTE
# ==========================================
if __name__ == "__main__":
    
    ticket_exemplo = """
    Comprei as peças com vocês mês passado para montar um servidor caseiro. 
    Coloquei um processador Xeon E3-1270 V2 numa placa-mãe H61 que eu já tinha. O PC liga os coolers, 
    mas dá tela preta direto, não bipa e não dá vídeo de jeito nenhum. A minha fonte é uma genérica 
    de 200W. Quero abrir um processo de devolução no juizado especial se vocês não trocarem a placa.
    """
    
    print("Iniciando análise do agente via Gemini (SDK Nativo)...\n")
    
    try:
        resultado_json = run_triage_agent(ticket_exemplo)
        
        print("--- RESULTADO DA TRIAGEM (JSON ESTRUTURADO) ---")
        
        # O resultado já vem como uma string JSON perfeita, vamos formatar para exibir no terminal
        objeto_python = json.loads(resultado_json)
        print(json.dumps(objeto_python, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Erro na execução: {e}")