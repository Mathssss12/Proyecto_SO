# ============================================================
#  gestor_de_misiones.py
#  Controla el flujo del tutorial paso a paso (Modo Guiado)
# ============================================================

class GestorDeMisiones:
    def __init__(self, activo: bool = False):
        self.activo = activo
        self.mision_actual = 1 if activo else 0
        self.textos = {
            1: "PASO 1: Observa el sistema. Haz clic en 'Enviar ola de estudiantes'.",
            2: "PASO 2: Tolerancia. Haz clic en 'Provocar un fallo' para tirar un nodo.",
            3: "PASO 3: Redundancia. Restaura el sistema usando 'Reparar servidor caído'.",
            4: "PASO 4: Balanceo. Libera a los estudiantes con 'Atender cola de espera'.",
            5: "¡TUTORIAL COMPLETADO! Haz clic en Ver Resultados Finales."
        }

    def obtener_instruccion(self) -> str:
        """Devuelve el texto de la misión actual."""
        if not self.activo:
            return ""
        return self.textos.get(self.mision_actual, "")

    def avanzar(self, paso_completado: int):
        """Avanza a la siguiente misión solo si se completó el paso requerido."""
        if self.activo and self.mision_actual == paso_completado:
            self.mision_actual += 1

    def completado(self) -> bool:
        """Verifica si el tutorial ha terminado."""
        return self.mision_actual >= 5

    def puede_ejecutar(self, paso_boton: int) -> bool:
        """Valida si un botón específico debe estar habilitado."""
        if not self.activo:
            return True  # En modo libre, todo está habilitado
        return self.mision_actual == paso_boton or self.completado()