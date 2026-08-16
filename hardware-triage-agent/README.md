#  HardwareTech Triage Agent (Multi-Agent Pipeline)

Um sistema corporativo de Inteligência Artificial baseado em múltiplos agentes (Multi-Agent System) para automação de Helpdesk, triagem técnica e mitigação de riscos jurídicos. 

Este projeto demonstra a orquestração de LLMs para transformar relatos não estruturados de clientes em dados tipados (JSON) e comunicações seguras para o ambiente empresarial.

##  Arquitetura do Sistema

A aplicação foi construída utilizando **LangGraph** para criar um fluxo determinístico de estado (StateGraph). O pipeline é composto por três agentes especializados operando em cadeia:

1. **Agent 1 (Triador Técnico):** Utiliza *Structured Outputs* (Pydantic) e *Chain-of-Thought* para analisar a falha de hardware, extrair as peças mencionadas e determinar o nível de urgência e departamento responsável.
2. **Agent 2 (Redator de Comunicação):** Consome o JSON técnico e o ticket original para redigir um e-mail de resposta empático e tecnicamente preciso.
3. **Agent 3 (Compliance & QA - LLM-as-a-Judge):** Atua como um auditor jurídico interno. Analisa o e-mail gerado pelo Agent 2 em busca de admissões indevidas de culpa (ex: passivos para o Juizado Especial Cível ou Procon) e reescreve o texto final garantindo segurança legal para a empresa.

##  Tecnologias Utilizadas

* **Motor LLM:** Google Gemini API (modelos da família Flash via SDK Nativo `google-generativeai`).
* **Orquestração de Agentes:** LangGraph.
* **Validação de Dados:** Pydantic (garantindo parsing de JSON infalível).
* **Backend (API):** FastAPI e Uvicorn.
* **Frontend (UI):** Streamlit.
* **Infraestrutura:** Preparado para conteinerização via Docker e Docker Compose.

##  Como Executar o Projeto Localmente

O projeto está dividido em microsserviços (Backend e Frontend). Para rodar no ambiente local sem o Docker, você precisará de dois terminais.

**1. Clone o repositório e instale as dependências:**
```bash
git clone [https://github.com/SEU-USUARIO/hardware-triage-agent.git](https://github.com/SEU-USUARIO/hardware-triage-agent.git)
cd hardware-triage-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements-api.txt
pip install -r requirements-web.txt