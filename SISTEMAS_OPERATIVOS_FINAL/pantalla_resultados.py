# ============================================================
#  pantalla_resultados.py
#  Pantalla de resultados finales y calificación
# ============================================================

import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_AMARILLO,
    COLOR_VERDE, COLOR_BORDE, COLOR_ROJO, COLOR_TEXTO,
    COLOR_TEXTO_SUAVE, FUENTE_SUBTIT, FUENTE_NORMAL
)
from componentes import BotonJuego
from estados import EstadoServidor
from sistema_de_matricula import SistemaDeMatricula


class PantallaResultados(tk.Frame):
    def __init__(self, parent, sistema: SistemaDeMatricula, al_salir):
        super().__init__(parent, bg=COLOR_FONDO)
        self.sistema  = sistema
        self.al_salir = al_salir
        self._construir()

    def _construir(self):
        redir  = self.sistema.balanceador.peticiones_redirigidas
        rechaz = self.sistema.balanceador.peticiones_rechazadas
        total  = redir + rechaz
        tasa   = (redir / total * 100) if total > 0 else 0
        caidos = sum(1 for s in self.sistema.servidores if s.estado == EstadoServidor.CAIDO)

        if self.sistema.estado_juego == "VICTORIA":
            calificacion = "🏆 MISIONES COMPLETADAS" if self.sistema.gestor_misiones.activo else "🏆 INFRAESTRUCTURA PERFECTA"
            color_cal    = COLOR_VERDE
            emoji_grande = "🏆"
        else:
            calificacion = "💀 COLAPSO TOTAL"
            color_cal    = COLOR_ROJO
            emoji_grande = "💀"

        tk.Frame(self, bg=color_cal, height=4).pack(fill="x")
        tk.Label(self, text=emoji_grande, font=("Courier New", 48), bg=COLOR_FONDO, fg=color_cal).pack(pady=(20, 0))
        tk.Label(self, text="RESULTADO FINAL", font=("Courier New", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE).pack()
        tk.Label(self, text=calificacion, font=("Courier New", 20, "bold"), bg=COLOR_FONDO, fg=color_cal).pack(pady=(4, 20))

        stats = tk.Frame(self, bg=COLOR_PANEL)
        stats.pack(padx=60, pady=10, fill="x")
        tk.Frame(stats, bg=color_cal, height=2).pack(fill="x")
        tk.Label(stats, text="RESUMEN DE TU SIMULACIÓN", font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=10).pack()

        for etiqueta, valor, color in [
            ("Servidores caídos al final", str(caidos),                      COLOR_ROJO if caidos > 0 else COLOR_VERDE),
            ("Algoritmo utilizado",        self.sistema.balanceador.algoritmo.value, COLOR_ACENTO),
            ("Estudiantes atendidos",      f"{redir}  ({tasa:.1f}%)",        COLOR_VERDE if tasa >= 80 else COLOR_AMARILLO),
            ("Aún en cola de espera",      str(len(self.sistema.cola_espera)), COLOR_AMARILLO),
        ]:
            fila = tk.Frame(stats, bg=COLOR_PANEL)
            fila.pack(fill="x", padx=20, pady=2)
            tk.Label(fila, text=etiqueta + ":", font=FUENTE_NORMAL, bg=COLOR_PANEL,
                     fg=COLOR_TEXTO_SUAVE, width=28, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=color).pack(side="left")

        tk.Frame(stats, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        BotonJuego(self, "SALIR DEL JUEGO", self.al_salir, color_acento=COLOR_TEXTO_SUAVE).pack(pady=20)