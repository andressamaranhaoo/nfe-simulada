from datetime import datetime
from pydantic import BaseModel, Field

from app.domain.enums.nfe_status import NfeStatus


class NfeCreateIn(BaseModel):
    emitente_cnpj: str = Field(min_length=14, max_length=14)
    destinatario_cnpj: str = Field(min_length=14, max_length=14)
    valor_total: float = Field(gt=0)


class NfeOut(BaseModel):
    id: str
    chave: str
    emitente_cnpj: str
    destinatario_cnpj: str
    valor_total: float
    status: NfeStatus
    created_at: datetime
