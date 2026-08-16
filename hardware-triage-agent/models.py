from pydantic import BaseModel, Field
from typing import List, Literal
import os
from dotenv import load_dotenv


class ActionItem(BaseModel):
    step: str = Field(description="Ação específica que deve ser tomada")
    assignee: Literal["L1_Support", "L2_Engineering", "Logistics", "Legal"] = Field(
        description="Departamento responsável por esta etapa"
    )

class TriageResponse(BaseModel):
    # A técnica de colocar o raciocínio PRIMEIRO no schema força o CoT (Chain-of-Thought)
    # O modelo gera os tokens de análise antes de gerar a classificação final.
    diagnostic_reasoning: str = Field(
        description="Análise técnica passo a passo do problema relatado pelo cliente. Pense em voz alta sobre possíveis causas."
    )
    issue_category: Literal["Hardware Failure", "Software/Driver", "Compatibility", "Warranty Claim"] = Field(
        description="Classificação principal do problema"
    )
    urgency_level: Literal["Low", "Medium", "High", "Critical"] = Field(
        description="Nível de urgência baseado no impacto sistêmico"
    )
    hardware_components_mentioned: List[str] = Field(
        description="Lista de peças mencionadas (ex: processador, placa-mãe, fonte)"
    )
    action_plan: List[ActionItem] = Field(
        description="Plano de ação recomendado para resolver o ticket"
    )