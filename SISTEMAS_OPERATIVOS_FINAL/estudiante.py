# ============================================================
#  estudiante.py
#  Representa a cada estudiante del portal
# ============================================================

from dataclasses import dataclass


@dataclass
class Estudiante:
    id: int
    nombre: str
    sesion_activa: bool = False
    matriculado: bool = False
    intentos: int = 0
    prioridad: int = 1  # 1 = normal, 2 = alta (ej: becados)

    def __str__(self):
        if self.matriculado:
            estado = "Matriculado"
        elif self.sesion_activa:
            estado = "En sesión"
        else:
            estado = "En espera"
        return (
            f"  Estudiante #{self.id:04d} | {self.nombre:<15} | "
            f"{estado} | Intentos: {self.intentos}"
        )