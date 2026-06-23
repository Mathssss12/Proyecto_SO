# ============================================================
#  gestor_de_sesiones.py
#  Maneja tokens de sesión para que ningún estudiante
#  pierda su progreso aunque cambie de servidor
# ============================================================

import random
from typing import Optional
from estudiante import Estudiante


class GestorDeSesiones:
    def __init__(self):
        self.sesiones_activas: dict = {}  # { estudiante_id: token }

    def iniciar_sesion(self, estudiante: Estudiante) -> str:
        token = f"TKN-{estudiante.id:04d}-{random.randint(1000, 9999)}"
        self.sesiones_activas[estudiante.id] = token
        estudiante.sesion_activa = True
        return token

    def validar_sesion(self, estudiante: Estudiante) -> bool:
        return estudiante.id in self.sesiones_activas

    def cerrar_sesion(self, estudiante: Estudiante):
        if estudiante.id in self.sesiones_activas:
            del self.sesiones_activas[estudiante.id]
            estudiante.sesion_activa = False

    def total_sesiones(self) -> int:
        return len(self.sesiones_activas)