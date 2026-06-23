# ============================================================
#  enums.py
#  Contiene todas las enumeraciones del sistema
# ============================================================

from enum import Enum


class EstadoServidor(Enum):
    ACTIVO   = "🟢 ACTIVO"
    SATURADO = "🟡 SATURADO"
    CAIDO    = "🔴 CAÍDO"


class AlgoritmoBalanceo(Enum):
    ROUND_ROBIN  = "Round Robin"
    PRIORIDAD    = "Por Prioridad"
    MENOR_CARGA  = "Menor Carga Primero"


class TipoFallo(Enum):
    SOBRECARGA  = "Sobrecarga de peticiones"
    HARDWARE    = "Fallo de hardware"
    SOFTWARE    = "Error de software"
    CIBERATAQUE = "Ciberataque (DDoS)"