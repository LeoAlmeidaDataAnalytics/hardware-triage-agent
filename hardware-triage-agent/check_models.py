import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Consultando a API do Google...\n")
print("Modelos disponíveis para geração de texto (generateContent):")

# Pede para a API listar todos os modelos liberados para a sua chave
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erro ao conectar com a API: {e}")