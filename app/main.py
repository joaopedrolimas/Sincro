from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import users, agendamentos, ia

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Login + Agendamento + IA",
    description="Exemplo completo com FastAPI, JWT, SQLAlchemy e OpenAI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(agendamentos.router)
app.include_router(ia.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "docs": "/docs"}