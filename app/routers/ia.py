from fastapi import APIRouter, Depends, HTTPException
from app.schemas import IAPergunta, IAResposta
from app.auth import get_current_user
from app.models import User
from app.config import settings
from openai import OpenAI

router = APIRouter(prefix="/ia", tags=["Assistente IA"])

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

SYSTEM_PROMPT = (
    "Você é um assistente virtual útil, objetivo e amigável. "
    "Responda sempre em português do Brasil."
)

@router.post("/perguntar", response_model=IAResposta)
def perguntar(dados: IAPergunta, user: User = Depends(get_current_user)):
    if not client:
        raise HTTPException(503, "Serviço de IA não configurado (OPENAI_API_KEY ausente)")
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": dados.pergunta},
            ],
            temperature=0.7,
        )
        return IAResposta(resposta=resp.choices[0].message.content)
    except Exception as e:
        raise HTTPException(500, f"Erro ao consultar IA: {e}")