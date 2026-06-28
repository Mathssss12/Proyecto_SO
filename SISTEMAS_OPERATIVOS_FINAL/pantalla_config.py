# ============================================================
#  pantalla_config.py
#  Pantalla de configuración de infraestructura
# ============================================================

import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_AMARILLO,
    COLOR_ROJO, COLOR_VERDE, COLOR_BORDE, COLOR_TEXTO,
    COLOR_TEXTO_SUAVE, COLOR_BOTON, COLOR_BOTON_HOVER,
    FUENTE_TITULO, FUENTE_SUBTIT, FUENTE_NORMAL, FUENTE_PEQUEÑA
)
from componentes import BotonJuego
from estados import AlgoritmoBalanceo


class PantallaConfiguracion(tk.Frame):
    def __init__(self, parent, al_continuar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.al_continuar   = al_continuar
        self.var_servidores = tk.IntVar(value=3)
        self.var_capacidad  = tk.IntVar(value=100)
        self.var_algoritmo  = tk.StringVar(value="1")
        self._construir()

    def _construir(self):
        tk.Label(
            self, text="CONFIGURA TU INFRAESTRUCTURA",
            font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(30, 4))

        tk.Label(
            self,
            text="Antes de abrir las matrículas, decide cómo será tu sistema de servidores.",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 20))

        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=40)

        izq = tk.Frame(contenedor, bg=COLOR_FONDO)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._panel_servidores(izq)
        self._panel_capacidad(izq)

        der = tk.Frame(contenedor, bg=COLOR_FONDO)
        der.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self._panel_algoritmo(der)

        BotonJuego(
            self, texto="CONFIRMAR Y COMENZAR",
            comando=self._confirmar, color_acento=COLOR_VERDE
        ).pack(pady=24)

    def _panel_servidores(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="x", pady=(0, 10))
        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")
        tk.Label(
            panel, text="🖥️  ¿CUÁNTOS SERVIDORES?",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=10
        ).pack()

        tk.Label(
            panel,
            text="1 servidor  →  Sin protección (igual al problema original)\n"
                 "3 servidores →  Protección básica  Recomendado\n"
                 "5 servidores →  Protección máxima",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO,
            justify="left", padx=16
        ).pack(anchor="w")

        frame_s = tk.Frame(panel, bg=COLOR_PANEL)
        frame_s.pack(fill="x", padx=16, pady=10)

        self.lbl_servidores = tk.Label(
            frame_s, text="3",
            font=("Courier New", 22, "bold"),
            bg=COLOR_PANEL, fg=COLOR_VERDE
        )
        self.lbl_servidores.pack(side="right", padx=10)

        tk.Scale(
            frame_s, from_=1, to=5, orient="horizontal",
            variable=self.var_servidores,
            command=lambda v: self.lbl_servidores.configure(text=v),
            bg=COLOR_PANEL, fg=COLOR_TEXTO, troughcolor=COLOR_BORDE,
            highlightthickness=0, activebackground=COLOR_ACENTO, length=200
        ).pack(side="left", fill="x", expand=True)

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x", pady=(6, 0))

    def _panel_capacidad(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="x", pady=(0, 10))
        tk.Frame(panel, bg=COLOR_AMARILLO, height=2).pack(fill="x")
        tk.Label(
            panel, text="¿CAPACIDAD POR SERVIDOR?",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=10
        ).pack()

        tk.Label(
            panel,
            text="¿Cuántos estudiantes puede atender cada servidor a la vez?\n"
                 "Más capacidad = más estudiantes simultáneos = más seguro.",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO,
            justify="left", padx=16
        ).pack(anchor="w")

        frame_c = tk.Frame(panel, bg=COLOR_PANEL)
        frame_c.pack(fill="x", padx=16, pady=10)

        self.lbl_capacidad = tk.Label(
            frame_c, text="100",
            font=("Courier New", 22, "bold"),
            bg=COLOR_PANEL, fg=COLOR_AMARILLO
        )
        self.lbl_capacidad.pack(side="right", padx=10)

        tk.Scale(
            frame_c, from_=50, to=500, resolution=50,
            orient="horizontal", variable=self.var_capacidad,
            command=lambda v: self.lbl_capacidad.configure(text=v),
            bg=COLOR_PANEL, fg=COLOR_TEXTO, troughcolor=COLOR_BORDE,
            highlightthickness=0, activebackground=COLOR_AMARILLO, length=200
        ).pack(side="left", fill="x", expand=True)

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x", pady=(6, 0))

    def _panel_algoritmo(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="both", expand=True)
        tk.Frame(panel, bg=COLOR_ROJO, height=2).pack(fill="x")
        tk.Label(
            panel, text="🔀  ALGORITMO DE BALANCEO",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ROJO, pady=10
        ).pack()
        tk.Label(
            panel, text="¿Cómo decides a qué servidor va cada estudiante?",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 10))

        for valor, nombre, desc in [
            ("1", "Round Robin",  "Turno rotativo entre servidores.\nEquitativo y simple.\n✅ Bueno para carga uniforme."),
            ("2", "Por Prioridad","Estudiantes becados y urgentes\nvan al servidor menos cargado.\n✅ Bueno para casos especiales."),
            ("3", "Menor Carga",  "Siempre envía al servidor\nmenos ocupado en ese momento.\n✅ Mejor distribución dinámica."),
        ]:
            f = tk.Frame(panel, bg=COLOR_BOTON, cursor="hand2")
            f.pack(fill="x", padx=12, pady=4)
            tk.Radiobutton(
                f, text=nombre, variable=self.var_algoritmo, value=valor,
                font=FUENTE_SUBTIT, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                selectcolor=COLOR_BORDE, activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_ACENTO, anchor="w"
            ).pack(fill="x", padx=10, pady=(8, 0))
            tk.Label(
                f, text=desc, font=FUENTE_PEQUEÑA,
                bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE,
                justify="left", padx=30
            ).pack(anchor="w", pady=(0, 8))

    def _confirmar(self):
        alg_map = {
            "1": AlgoritmoBalanceo.ROUND_ROBIN,
            "2": AlgoritmoBalanceo.PRIORIDAD,
            "3": AlgoritmoBalanceo.MENOR_CARGA
        }
        self.al_continuar(
            self.var_servidores.get(),
            self.var_capacidad.get(),
            alg_map[self.var_algoritmo.get()]
        )