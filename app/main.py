from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4

app = FastAPI(title="API NF-e Simulada")

# "Banco" em memória
DB_NFE = []

class NFCreate(BaseModel):
    id_notafiscal: Optional[str] = None
    empresa_nome: str
    empresa_cnpj: str
    emitente_nome: str
    destinatario_nome: str
    valor_total: float

class NF(NFCreate):
    chave: str
    status: str = "Emitida"

@app.get("/")
def root():
    return {"status": "API NF-e OK"}

@app.post("/nfe/", response_model=NF)
def criar_nf(payload: NFCreate):
    chave = str(uuid4())

    nf = NF(
        **payload.dict(),
        chave=chave,
        status="Emitida"
    )

    DB_NFE.append(nf)
    return nf

@app.get("/nfe/", response_model=List[NF])
def listar_nfe():
    return DB_NFE

@app.get("/nfe/{chave}", response_model=NF)
def consultar_nf(chave: str):
    for nf in DB_NFE:
        if nf.chave == chave or nf.id_notafiscal == chave:
            return nf
    raise HTTPException(status_code=404, detail="NF não encontrada")

@app.post("/nfe/{chave}/cancelar")
def cancelar_nf(chave: str):
    for nf in DB_NFE:
        if nf.chave == chave:
            nf.status = "Cancelada"
            return {"mensagem": "NF cancelada", "chave": chave}
    raise HTTPException(status_code=404, detail="NF não encontrada")
