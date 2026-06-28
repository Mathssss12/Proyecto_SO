# ============================================================
#  componentes.py
#  Widgets reutilizables: BotonJuego y PanelModalInterno
# ============================================================

import tkinter as tk
from estilos import (
    COLOR_BOTON, COLOR_BOTON_HOVER, COLOR_ACENTO,
    COLOR_PANEL, COLOR_FONDO, FUENTE_SUBTIT
)


class BotonJuego(tk.Button):
    def __init__(self, parent, texto, comando, color_acento=None, **kwargs):
        self.color_acento = color_acento or COLOR_ACENTO
        super().__init__(
            parent, text=texto, command=comando,
            bg=COLOR_BOTON, fg=self.color_acento,
            activebackground=COLOR_BOTON_HOVER,
            activeforeground=self.color_acento,
            font=FUENTE_SUBTIT, relief="flat", bd=0,
            padx=16, pady=10, cursor="hand2", **kwargs
        )
        self.bind("<Enter>", lambda e: self.configure(bg=COLOR_BOTON_HOVER) if self['state'] != 'disabled' else None)
        self.bind("<Leave>", lambda e: self.configure(bg=COLOR_BOTON) if self['state'] != 'disabled' else None)


class PanelModalInterno(tk.Frame):
    def __init__(self, parent, titulo: str, color_borde=COLOR_ACENTO, width=550, height=450):
        super().__init__(parent, bg=COLOR_FONDO, bd=2, relief="solid", highlightbackground=color_borde)
        self.place(relx=0.5, rely=0.5, anchor="center", width=width, height=height)

        self.cabecera = tk.Frame(self, bg=COLOR_PANEL)
        self.cabecera.pack(fill="x")
        tk.Frame(self.cabecera, bg=color_borde, height=3).pack(fill="x")
        tk.Label(
            self.cabecera, text=titulo,
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=color_borde, pady=10
        ).pack(side="left", padx=15)

        self.cuerpo = tk.Frame(self, bg=COLOR_FONDO)
        self.cuerpo.pack(fill="both", expand=True, padx=20, pady=15)