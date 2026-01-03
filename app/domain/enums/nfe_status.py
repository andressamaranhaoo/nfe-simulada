from enum import Enum


class NfeStatus(str, Enum):
    EMITIDA = "EMITIDA"
    CANCELADA = "CANCELADA"
    REJEITADA = "REJEITADA"
