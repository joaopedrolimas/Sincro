from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    agendamentos = relationship("Agendamento", back_populates="usuario")

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    data_hora = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="agendamentos")