# ============================================================
#  balanceador_de_carga.py
#  Distribuye peticiones entre servidores según el algoritmo
# ============================================================

from typing import List, Optional
from estados import AlgoritmoBalanceo
from estudiante import Estudiante
from servidor_web import ServidorWeb


class BalanceadorDeCarga:
    def __init__(self, algoritmo: AlgoritmoBalanceo):
        self.algoritmo = algoritmo
        self.indice_round_robin = 0
        self.peticiones_redirigidas = 0
        self.peticiones_rechazadas = 0

    def asignar(self, servidores: List[ServidorWeb], estudiante: Estudiante) -> Optional[ServidorWeb]:
        disponibles = [s for s in servidores if s.tiene_espacio()]

        if not disponibles:
            self.peticiones_rechazadas += 1
            return None

        if self.algoritmo == AlgoritmoBalanceo.ROUND_ROBIN:
            servidor = self._round_robin(disponibles)
        elif self.algoritmo == AlgoritmoBalanceo.PRIORIDAD:
            servidor = self._por_prioridad(disponibles, estudiante)
        elif self.algoritmo == AlgoritmoBalanceo.MENOR_CARGA:
            servidor = self._menor_carga(disponibles)
        else:
            servidor = disponibles[0]

        if servidor and servidor.recibir_peticion():
            self.peticiones_redirigidas += 1
            return servidor

        self.peticiones_rechazadas += 1
        return None

    def _round_robin(self, disponibles: List[ServidorWeb]) -> ServidorWeb:
        self.indice_round_robin = self.indice_round_robin % len(disponibles)
        servidor = disponibles[self.indice_round_robin]
        self.indice_round_robin += 1
        return servidor

    def _por_prioridad(self, disponibles: List[ServidorWeb], estudiante: Estudiante) -> ServidorWeb:
        if estudiante.prioridad == 2:
            return min(disponibles, key=lambda s: s.peticiones_actuales)
        return disponibles[0]

    def _menor_carga(self, disponibles: List[ServidorWeb]) -> ServidorWeb:
        return min(disponibles, key=lambda s: s.peticiones_actuales)