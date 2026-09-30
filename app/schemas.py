from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#     Usuario 

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    is_admin: bool
    criado_em: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

#    Agendamento

class AgendamentoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_hora: datetime

class AgendamentoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_hora: Optional[datetime] = None

class AgendamentoOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    data_hora: datetime
    user_id: int
    criado_em: datetime

    class Config:
        from_attributes = True

# IA

class IAPergunta(BaseModel):
    pergunta: str

class IAResposta(BaseModel):
    resposta: str