from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from app.domain.enums.nfe_status import NfeStatus

Base = declarative_base()


class NfeModel(Base):
    __tablename__ = "nfes"

    chave = Column(String, primary_key=True, index=True)
    emitente = Column(String, nullable=False)
    destinatario = Column(String, nullable=False)
    valor_total = Column(String, nullable=False)
    status = Column(Enum(NfeStatus), nullable=False)
    criada_em = Column(DateTime, default=datetime.utcnow)
