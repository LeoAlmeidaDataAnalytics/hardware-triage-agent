import os
import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="HardwareTech - Triagem IA",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Portal de Triagem Automática (Nível 3)")
st.markdown("Insira o relato do cliente abaixo para gerar o diagnóstico e o e-mail auditado pelo sistema Multi-Agente.")

# URL da nossa FastAPI (Puxa do Docker ou usa localhost como padrão)
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1/triage")

# Área de texto para o ticket
ticket_text = st.text_area(
    "Relato do Cliente:",
    height=150,
    placeholder="Cole aqui o e-mail ou mensagem enviada pelo cliente..."
)

# Botão de ação
if st.button("Processar com Inteligência Artificial", type="primary"):
    if not ticket_text.strip():
        st.warning("Por favor, insira um relato válido antes de processar.")
    else:
        with st.spinner("Acionando a esteira de agentes (Triagem -> Redação -> Compliance)..."):
            try:
                # Dispara a requisição POST para a nossa FastAPI
                resposta = requests.post(
                    API_URL, 
                    json={"ticket_text": ticket_text}
                )
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    
                    st.success("Ticket processado e auditado com sucesso!")
                    
                    # Organizando a visualização em colunas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🔎 Relatório de Compliance")
                        st.info(dados["risco_legal_identificado"])
                        
                    with col2:
                        st.subheader("📩 E-mail Final (Aprovado)")
                        st.text_area(
                            "Pronto para envio:", 
                            value=dados["email_auditado_para_envio"], 
                            height=350, 
                            disabled=True
                        )
                else:
                    st.error(f"Erro na API: {resposta.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Falha ao conectar com a API. Verifique se o servidor backend está rodando.")