from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Agendamento, User
from app.schemas import AgendamentoCreate, AgendamentoUpdate, AgendamentoOut
from app.auth import get_current_user

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoOut, status_code=201)
def Criar(dados: AgendamentoCreate, db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    ag = Agendamento(**dados.model_dump(), user_id=user.id)
    db.add(ag)
    db.commit()
    db.refresh(ag)
    return ag

@router.get("/", response_model=List[AgendamentoOut])
def listar(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Agendamento).filter(Agendamento.user_id == user.id).all()

@router.get("/{ag_id}", response_model=AgendamentoOut)
def obter(ag_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ag = db.query(Agendamento).filter(Agendamento.id == ag_id, 
                                      Agendamento.user_id == user.id).first()
    if not ag:
        raise  HTTPException(404, "Agendamento não encontrado")
    return ag

@router.put("/{ag_id}", response_model=AgendamentoOut)
def atualizar(ag_id: int, dados: AgendamentoUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ag = db.query(Agendamento).filter(Agendamento.id == ag_id,
                                      Agendamento.user_id == user.id).first()
    if not ag:
        raise HTTPException(404, "Agendamento não encontrado")
    for k, v in dados.model_dump(exclude_unset=True).items():
        setattr(ag, k, v)

    db.commit()
    db.refresh(ag)
    return ag

@router.delete("/{ag_id}", status_code=204)
def deletar(ag_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ag = db.query(Agendamento).filter(Agendamento.id == ag_id,
                                      Agendamento.user_id == user.id).first()
    if not ag:
        raise HTTPException(404, "Agandamento não encontrado")
    db.delete(ag)
    db.commit()