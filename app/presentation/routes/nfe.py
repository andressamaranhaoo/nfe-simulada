from fastapi import APIRouter, HTTPException

from app.application.schemas.nfe import NfeCreateIn, NfeOut
from app.domain.entities.nfe import Nfe
from app.domain.enums.nfe_status import NfeStatus

router = APIRouter(prefix="/nfe", tags=["NF-e"])

# "banco" em memória (por enquanto)
DB = {}


@router.post("/", response_model=NfeOut)
def criar_nfe(payload: NfeCreateIn):
    nfe = Nfe.criar(
        emitente_cnpj=payload.emitente_cnpj,
        destinatario_cnpj=payload.destinatario_cnpj,
        valor_total=payload.valor_total,
    )
    DB[nfe.chave] = nfe
    return nfe


@router.get("/", response_model=list[NfeOut])
def listar_nfe():
    return list(DB.values())


@router.get("/{chave}", response_model=NfeOut)
def consultar_por_chave(chave: str):
    nfe = DB.get(chave)
    if not nfe:
        raise HTTPException(status_code=404, detail="NF-e não encontrada")
    return nfe


@router.post("/{chave}/cancelar", response_model=NfeOut)
def cancelar_nfe(chave: str):
    nfe = DB.get(chave)
    if not nfe:
        raise HTTPException(status_code=404, detail="NF-e não encontrada")
    if nfe.status == NfeStatus.CANCELADA:
        raise HTTPException(status_code=400, detail="NF-e já está cancelada")

    nfe.status = NfeStatus.CANCELADA
    DB[chave] = nfe
    return nfe
