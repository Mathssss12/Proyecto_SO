# ============================================================
#  servidor_web.py
#  Modela un servidor web con capacidad, carga y estado
# ============================================================

from dataclasses import dataclass, field
from estados import EstadoServidor


@dataclass
class ServidorWeb:
    id: int
    capacidad_maxima: int = 100
    peticiones_actuales: int = 0
    estado: EstadoServidor = field(default=EstadoServidor.ACTIVO)
    peticiones_procesadas: int = 0

    def tiene_espacio(self) -> bool:
        return (
            self.estado == EstadoServidor.ACTIVO and
            self.peticiones_actuales < self.capacidad_maxima
        )

    def recibir_peticion(self) -> bool:
        if self.tiene_espacio():
            self.peticiones_actuales += 1
            if self.peticiones_actuales >= self.capacidad_maxima * 0.85:
                self.estado = EstadoServidor.SATURADO
            return True
        return False

    def procesar_peticion(self) -> bool:
        if self.peticiones_actuales > 0:
            self.peticiones_actuales -= 1
            self.peticiones_procesadas += 1
            if self.peticiones_actuales < self.capacidad_maxima * 0.85:
                self.estado = EstadoServidor.ACTIVO
            return True
        return False

    def aplicar_fallo(self):
        self.estado = EstadoServidor.CAIDO
        self.peticiones_actuales = 0

    def recuperar(self):
        self.estado = EstadoServidor.ACTIVO
        self.peticiones_actuales = 0

    def _barra_carga(self) -> str:
        porcentaje = self.peticiones_actuales / self.capacidad_maxima
        llenos = int(porcentaje * 10)
        return "[" + "█" * llenos + "░" * (10 - llenos) + "]"

    def __str__(self):
        barra = self._barra_carga()
        return (
            f"  Servidor #{self.id} | {self.estado.value:<18} | "
            f"Carga: {barra} {self.peticiones_actuales}/{self.capacidad_maxima} | "
            f"Procesadas: {self.peticiones_procesadas}"
        )