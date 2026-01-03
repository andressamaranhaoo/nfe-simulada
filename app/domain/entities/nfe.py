from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.domain.enums.nfe_status import NfeStatus


@dataclass
class Nfe:
    id: str
    chave: str
    emitente_cnpj: str
    destinatario_cnpj: str
    valor_total: float
    status: NfeStatus
    created_at: datetime

    @staticmethod
    def criar(emitente_cnpj: str, destinatario_cnpj: str, valor_total: float) -> "Nfe":
        # chave simulada: 44 dígitos fake (aqui simplificado com UUID)
        chave = uuid4().hex.upper()[:44].ljust(44, "0")
        return Nfe(
            id=str(uuid4()),
            chave=chave,
            emitente_cnpj=emitente_cnpj,
            destinatario_cnpj=destinatario_cnpj,
            valor_total=valor_total,
            status=NfeStatus.EMITIDA,
            created_at=datetime.utcnow(),
        )
