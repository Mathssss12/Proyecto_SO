# ============================================================
#  pantalla_bienvenida.py
#  Primera pantalla: historia y elección de modo
# ============================================================

import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_AMARILLO,
    COLOR_VERDE, COLOR_BORDE, COLOR_TEXTO, COLOR_TEXTO_SUAVE,
    FUENTE_SUBTIT, FUENTE_NORMAL, FUENTE_PEQUEÑA
)
from componentes import BotonJuego


class PantallaBienvenida(tk.Frame):
    def __init__(self, parent, al_continuar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.al_continuar = al_continuar
        self._construir()

    def _construir(self):
        tk.Label(
            self, text="🎓 SIMULADOR DE MATRÍCULAS",
            font=("Courier New", 22, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(50, 4))

        tk.Label(
            self, text="UNIVERSITARIAS",
            font=("Courier New", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(0, 6))

        tk.Label(
            self, text="Sistemas Operativos — ITIZ2100",
            font=FUENTE_PEQUEÑA, bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 20))

        panel = tk.Frame(self, bg=COLOR_PANEL, bd=0)
        panel.pack(padx=60, pady=10, fill="x")
        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")

        tk.Label(
            panel, text="¿QUÉ ESTÁ PASANDO?",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=12
        ).pack()

        historia = (
            "Son las 08:00 AM. La universidad abre el proceso de matrícula\n"
            "para 15.000 estudiantes.\nEn segundos, miles intentan conectarse\n"
            "al mismo tiempo... y el portal colapsa por completo.\n\n"
            "Los estudiantes pierden su sesión. Nadie puede matricularse.\n"
            "El sistema no aguantó la carga."
        )
        tk.Label(
            panel, text=historia, font=FUENTE_NORMAL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO, justify="center", pady=10
        ).pack()

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x")

        tk.Label(
            panel, text="TU MISIÓN",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_VERDE, pady=12
        ).pack()

        mision = (
            "Diseña la infraestructura correcta, elige cómo distribuir\n"
            "el tráfico y gestiona los fallos en tiempo real.\n"
            "¡Evita el colapso y logra que todos los estudiantes\n"
            "puedan matricularse sin perder su sesión!"
        )
        tk.Label(
            panel, text=mision, font=FUENTE_NORMAL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO, justify="center", pady=10
        ).pack()

        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")

        frame_modos = tk.Frame(self, bg=COLOR_FONDO)
        frame_modos.pack(pady=20)

        BotonJuego(
            frame_modos, "▶ MODO GUIADO (TUTORIAL)",
            lambda: self.al_continuar(True), COLOR_VERDE
        ).pack(side="left", padx=10)

        BotonJuego(
            frame_modos, "▶ MODO LIBRE",
            lambda: self.al_continuar(False), COLOR_ACENTO
        ).pack(side="left", padx=10)