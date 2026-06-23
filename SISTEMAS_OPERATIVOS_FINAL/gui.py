# ============================================================
#  gui.py
#  Interfaz gráfica del simulador — estilo videojuego
#  Tkinter (incluido en Python, sin instalación extra)
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Optional, List

from estados import AlgoritmoBalanceo, TipoFallo, EstadoServidor
from estudiante import Estudiante
from sistema_de_matricula import SistemaDeMatricula

# ── Paleta de colores ─────────────────────────────────────
COLOR_FONDO         = "#0D0F1A"   # azul noche casi negro
COLOR_PANEL         = "#141828"   # panel ligeramente más claro
COLOR_BORDE         = "#1E3A5F"   # azul acero
COLOR_ACENTO        = "#00D4FF"   # cian neón (color principal)
COLOR_VERDE         = "#00FF88"   # verde éxito
COLOR_AMARILLO      = "#FFD700"   # amarillo advertencia
COLOR_ROJO          = "#FF4455"   # rojo peligro
COLOR_TEXTO         = "#E8EAF6"   # blanco lavanda
COLOR_TEXTO_SUAVE   = "#7B8BB2"   # gris azulado
COLOR_BOTON         = "#1A2744"   # fondo botón
COLOR_BOTON_HOVER   = "#243460"   # fondo botón hover

FUENTE_TITULO  = ("Courier New", 18, "bold")
FUENTE_SUBTIT  = ("Courier New", 12, "bold")
FUENTE_NORMAL  = ("Courier New", 10)
FUENTE_GRANDE  = ("Courier New", 14, "bold")
FUENTE_PEQUEÑA = ("Courier New", 9)

NOMBRES = [
    "Ana Torres", "Luis Pérez", "María García", "Carlos Ruiz", "Sofía Mora",
    "Diego Vega", "Valentina Cruz", "Andrés León", "Camila Ríos", "Pablo Díaz",
    "Isabella Muñoz", "Sebastián Lara", "Lucía Flores", "Mateo Herrera", "Daniela Romero",
    "Joaquín Silva", "Natalia Gómez", "Emilio Vargas", "Fernanda Castro", "Tomás Jiménez"
]


# ─────────────────────────────────────────────
#  WIDGET: Botón de juego personalizado
# ─────────────────────────────────────────────

class BotonJuego(tk.Button):
    def __init__(self, parent, texto, comando, color_acento=None, **kwargs):
        self.color_acento = color_acento or COLOR_ACENTO
        super().__init__(
            parent,
            text=texto,
            command=comando,
            bg=COLOR_BOTON,
            fg=self.color_acento,
            activebackground=COLOR_BOTON_HOVER,
            activeforeground=self.color_acento,
            font=FUENTE_SUBTIT,
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            **kwargs
        )
        self.bind("<Enter>", self._hover_on)
        self.bind("<Leave>", self._hover_off)

    def _hover_on(self, e):
        self.configure(bg=COLOR_BOTON_HOVER)

    def _hover_off(self, e):
        self.configure(bg=COLOR_BOTON)


# ─────────────────────────────────────────────
#  PANTALLA: Bienvenida
# ─────────────────────────────────────────────

class PantallaBienvenida(tk.Frame):
    def __init__(self, parent, al_continuar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.al_continuar = al_continuar
        self._construir()

    def _construir(self):
        # Título principal
        tk.Label(
            self,
            text="🎓 SIMULADOR DE MATRÍCULAS",
            font=("Courier New", 22, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(50, 4))

        tk.Label(
            self,
            text="UNIVERSITARIAS",
            font=("Courier New", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(0, 6))

        tk.Label(
            self,
            text="Sistemas Operativos — ITIZ2100",
            font=FUENTE_PEQUEÑA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 30))

        # Panel historia
        panel = tk.Frame(self, bg=COLOR_PANEL, bd=0)
        panel.pack(padx=60, pady=10, fill="x")

        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")

        tk.Label(
            panel,
            text="📖  ¿QUÉ ESTÁ PASANDO?",
            font=FUENTE_SUBTIT,
            bg=COLOR_PANEL, fg=COLOR_AMARILLO,
            pady=12
        ).pack()

        historia = (
            "Son las 08:00 AM. La universidad abre el proceso de matrícula\n"
            "para 15.000 estudiantes. En segundos, miles intentan conectarse\n"
            "al mismo tiempo... y el portal colapsa por completo.\n\n"
            "Los estudiantes pierden su sesión. Nadie puede matricularse.\n"
            "El sistema no aguantó la carga."
        )
        tk.Label(
            panel,
            text=historia,
            font=FUENTE_NORMAL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
            justify="center", pady=10
        ).pack()

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x")

        tk.Label(
            panel,
            text="🎯  TU MISIÓN",
            font=FUENTE_SUBTIT,
            bg=COLOR_PANEL, fg=COLOR_VERDE,
            pady=12
        ).pack()

        mision = (
            "Diseña la infraestructura correcta, elige cómo distribuir\n"
            "el tráfico y gestiona los fallos en tiempo real.\n"
            "¡Evita el colapso y logra que todos los estudiantes\n"
            "puedan matricularse sin perder su sesión!"
        )
        tk.Label(
            panel,
            text=mision,
            font=FUENTE_NORMAL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
            justify="center", pady=10
        ).pack()

        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")

        # Tip para principiantes
        tk.Label(
            self,
            text="💡  ¿Primera vez? No te preocupes — el juego te guía en cada paso.",
            font=FUENTE_PEQUEÑA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE,
            pady=16
        ).pack()

        BotonJuego(
            self,
            texto="▶   COMENZAR JUEGO",
            comando=self.al_continuar,
            color_acento=COLOR_VERDE
        ).pack(pady=10)


# ─────────────────────────────────────────────
#  PANTALLA: Configuración
# ─────────────────────────────────────────────

class PantallaConfiguracion(tk.Frame):
    def __init__(self, parent, al_continuar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.al_continuar = al_continuar
        self.var_servidores  = tk.IntVar(value=3)
        self.var_capacidad   = tk.IntVar(value=100)
        self.var_algoritmo   = tk.StringVar(value="1")
        self._construir()

    def _construir(self):
        tk.Label(
            self,
            text="⚙️  CONFIGURA TU INFRAESTRUCTURA",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(30, 4))

        tk.Label(
            self,
            text="Antes de abrir las matrículas, decide cómo será tu sistema de servidores.",
            font=FUENTE_NORMAL,
            bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 20))

        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=40)

        # ── Columna izquierda: servidores y capacidad
        izq = tk.Frame(contenedor, bg=COLOR_FONDO)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._panel_servidores(izq)
        self._panel_capacidad(izq)

        # ── Columna derecha: algoritmo
        der = tk.Frame(contenedor, bg=COLOR_FONDO)
        der.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self._panel_algoritmo(der)

        # Botón continuar
        BotonJuego(
            self,
            texto="✅   CONFIRMAR Y COMENZAR",
            comando=self._confirmar,
            color_acento=COLOR_VERDE
        ).pack(pady=24)

    def _panel_servidores(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="x", pady=(0, 10))
        tk.Frame(panel, bg=COLOR_ACENTO, height=2).pack(fill="x")

        tk.Label(
            panel, text="🖥️  ¿CUÁNTOS SERVIDORES?",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=10
        ).pack()

        ayuda = (
            "1 servidor  →  Sin protección (igual al problema original)\n"
            "3 servidores →  Protección básica  ✅  Recomendado\n"
            "5 servidores →  Protección máxima"
        )
        tk.Label(
            panel, text=ayuda, font=FUENTE_PEQUEÑA,
            bg=COLOR_PANEL, fg=COLOR_TEXTO, justify="left", padx=16
        ).pack(anchor="w")

        frame_slider = tk.Frame(panel, bg=COLOR_PANEL)
        frame_slider.pack(fill="x", padx=16, pady=10)

        self.lbl_servidores = tk.Label(
            frame_slider, text="3",
            font=("Courier New", 22, "bold"),
            bg=COLOR_PANEL, fg=COLOR_VERDE
        )
        self.lbl_servidores.pack(side="right", padx=10)

        slider = tk.Scale(
            frame_slider,
            from_=1, to=5,
            orient="horizontal",
            variable=self.var_servidores,
            command=self._actualizar_lbl_servidores,
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
            troughcolor=COLOR_BORDE,
            highlightthickness=0,
            activebackground=COLOR_ACENTO,
            length=200
        )
        slider.pack(side="left", fill="x", expand=True)

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x", pady=(6, 0))

    def _actualizar_lbl_servidores(self, val):
        self.lbl_servidores.configure(text=val)

    def _panel_capacidad(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="x", pady=(0, 10))
        tk.Frame(panel, bg=COLOR_AMARILLO, height=2).pack(fill="x")

        tk.Label(
            panel, text="📦  ¿CAPACIDAD POR SERVIDOR?",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=10
        ).pack()

        ayuda = (
            "¿Cuántos estudiantes puede atender cada servidor a la vez?\n"
            "Más capacidad = más estudiantes simultáneos = más seguro."
        )
        tk.Label(
            panel, text=ayuda, font=FUENTE_PEQUEÑA,
            bg=COLOR_PANEL, fg=COLOR_TEXTO, justify="left", padx=16
        ).pack(anchor="w")

        frame_slider = tk.Frame(panel, bg=COLOR_PANEL)
        frame_slider.pack(fill="x", padx=16, pady=10)

        self.lbl_capacidad = tk.Label(
            frame_slider, text="100",
            font=("Courier New", 22, "bold"),
            bg=COLOR_PANEL, fg=COLOR_AMARILLO
        )
        self.lbl_capacidad.pack(side="right", padx=10)

        slider = tk.Scale(
            frame_slider,
            from_=50, to=500, resolution=50,
            orient="horizontal",
            variable=self.var_capacidad,
            command=self._actualizar_lbl_capacidad,
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
            troughcolor=COLOR_BORDE,
            highlightthickness=0,
            activebackground=COLOR_AMARILLO,
            length=200
        )
        slider.pack(side="left", fill="x", expand=True)

        tk.Frame(panel, bg=COLOR_BORDE, height=1).pack(fill="x", pady=(6, 0))

    def _actualizar_lbl_capacidad(self, val):
        self.lbl_capacidad.configure(text=val)

    def _panel_algoritmo(self, parent):
        panel = tk.Frame(parent, bg=COLOR_PANEL)
        panel.pack(fill="both", expand=True)
        tk.Frame(panel, bg=COLOR_ROJO, height=2).pack(fill="x")

        tk.Label(
            panel, text="🔀  ALGORITMO DE BALANCEO",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ROJO, pady=10
        ).pack()

        tk.Label(
            panel,
            text="¿Cómo decides a qué servidor va cada estudiante?",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 10))

        opciones = [
            ("1", "🔄  Round Robin",
             "Turno rotativo entre servidores.\nEquitativo y simple.\n✅ Bueno para carga uniforme."),
            ("2", "⭐  Por Prioridad",
             "Estudiantes becados y urgentes\nvan al servidor menos cargado.\n✅ Bueno para casos especiales."),
            ("3", "⚖️  Menor Carga",
             "Siempre envía al servidor\nmenos ocupado en ese momento.\n✅ Mejor distribución dinámica."),
        ]

        for valor, nombre, desc in opciones:
            f = tk.Frame(panel, bg=COLOR_BOTON, cursor="hand2")
            f.pack(fill="x", padx=12, pady=4)

            rb = tk.Radiobutton(
                f,
                text=nombre,
                variable=self.var_algoritmo,
                value=valor,
                font=FUENTE_SUBTIT,
                bg=COLOR_BOTON, fg=COLOR_TEXTO,
                selectcolor=COLOR_BORDE,
                activebackground=COLOR_BOTON_HOVER,
                activeforeground=COLOR_ACENTO,
                anchor="w"
            )
            rb.pack(fill="x", padx=10, pady=(8, 0))

            tk.Label(
                f, text=desc,
                font=FUENTE_PEQUEÑA,
                bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE,
                justify="left", padx=30
            ).pack(anchor="w", pady=(0, 8))

    def _confirmar(self):
        algoritmo_map = {
            "1": AlgoritmoBalanceo.ROUND_ROBIN,
            "2": AlgoritmoBalanceo.PRIORIDAD,
            "3": AlgoritmoBalanceo.MENOR_CARGA
        }
        self.al_continuar(
            self.var_servidores.get(),
            self.var_capacidad.get(),
            algoritmo_map[self.var_algoritmo.get()]
        )


# ─────────────────────────────────────────────
#  PANTALLA: Juego principal
# ─────────────────────────────────────────────

class PantallaJuego(tk.Frame):
    def __init__(self, parent, sistema: SistemaDeMatricula, al_finalizar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.sistema      = sistema
        self.al_finalizar = al_finalizar
        self.contador_id  = 1
        self._construir()
        self._actualizar_vista()

    def _construir(self):
        # ── Cabecera ──────────────────────────────────────────
        cabecera = tk.Frame(self, bg=COLOR_PANEL)
        cabecera.pack(fill="x")
        tk.Frame(cabecera, bg=COLOR_ACENTO, height=3).pack(fill="x")

        tk.Label(
            cabecera,
            text="🎓  PORTAL DE MATRÍCULAS — SALA DE CONTROL",
            font=FUENTE_TITULO,
            bg=COLOR_PANEL, fg=COLOR_ACENTO,
            pady=10
        ).pack()

        tk.Frame(cabecera, bg=COLOR_BORDE, height=1).pack(fill="x")

        # ── Cuerpo principal ──────────────────────────────────
        cuerpo = tk.Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)

        # Columna izquierda: servidores + métricas
        izq = tk.Frame(cuerpo, bg=COLOR_FONDO)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self._panel_servidores(izq)
        self._panel_metricas(izq)

        # Columna derecha: acciones + log
        der = tk.Frame(cuerpo, bg=COLOR_FONDO)
        der.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self._panel_acciones(der)
        self._panel_log(der)

    # ── Paneles de información ────────────────────────────────

    def _panel_servidores(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_ACENTO, height=2).pack(fill="x")

        tk.Label(
            frame, text="🖥️  ESTADO DE TUS SERVIDORES",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=8
        ).pack()

        self.frame_servidores_interno = tk.Frame(frame, bg=COLOR_PANEL)
        self.frame_servidores_interno.pack(fill="x", padx=10, pady=(0, 10))

    def _panel_metricas(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_VERDE, height=2).pack(fill="x")

        tk.Label(
            frame, text="📊  MÉTRICAS EN TIEMPO REAL",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_VERDE, pady=8
        ).pack()

        grid = tk.Frame(frame, bg=COLOR_PANEL)
        grid.pack(fill="x", padx=10, pady=(0, 10))

        self.lbl_sesiones   = self._metrica(grid, "Sesiones activas",    "0",  COLOR_VERDE,    0)
        self.lbl_cola       = self._metrica(grid, "En cola de espera",   "0",  COLOR_AMARILLO, 1)
        self.lbl_atendidas  = self._metrica(grid, "Peticiones atendidas","0",  COLOR_ACENTO,   2)
        self.lbl_rechazadas = self._metrica(grid, "Peticiones rechazadas","0", COLOR_ROJO,     3)
        self.lbl_tasa       = self._metrica(grid, "Tasa de éxito",       "—",  COLOR_VERDE,    4)

    def _metrica(self, parent, etiqueta, valor_inicial, color, col):
        f = tk.Frame(parent, bg=COLOR_BOTON)
        f.grid(row=0, column=col, padx=4, pady=4, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(f, text=valor_inicial, font=("Courier New", 18, "bold"),
                 bg=COLOR_BOTON, fg=color).pack(pady=(8, 0))
        tk.Label(f, text=etiqueta, font=FUENTE_PEQUEÑA,
                 bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE).pack(pady=(0, 8))
        return f.winfo_children()[0]  # retorna el label del número

    def _panel_acciones(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_AMARILLO, height=2).pack(fill="x")

        tk.Label(
            frame, text="🕹️  ACCIONES DISPONIBLES",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=8
        ).pack()

        tk.Label(
            frame,
            text="Haz clic en una acción para ejecutarla:",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE
        ).pack(pady=(0, 8))

        acciones = [
            ("📥  Enviar ola de estudiantes",
             "Simula que llegan estudiantes\nal portal al mismo tiempo.",
             self._accion_estudiantes, COLOR_ACENTO),

            ("💥  Provocar un fallo",
             "Simula un fallo inesperado\nen uno de tus servidores.",
             self._accion_fallo, COLOR_ROJO),

            ("🔧  Reparar servidor caído",
             "Vuelve a poner en línea\nun servidor que falló.",
             self._accion_reparar, COLOR_VERDE),

            ("♻️  Atender cola de espera",
             "Reintenta conectar a los\nestudiantes que esperan.",
             self._accion_cola, COLOR_AMARILLO),

            ("🏁  Ver resultados finales",
             "Termina la simulación\ny ve tu calificación.",
             self.al_finalizar, COLOR_TEXTO_SUAVE),
        ]

        for texto, tooltip, comando, color in acciones:
            f = tk.Frame(frame, bg=COLOR_BOTON)
            f.pack(fill="x", padx=10, pady=3)

            BotonJuego(f, texto=texto, comando=comando, color_acento=color).pack(
                side="left", padx=(0, 8)
            )
            tk.Label(
                f, text=tooltip, font=FUENTE_PEQUEÑA,
                bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE, justify="left"
            ).pack(side="left", pady=6)

    def _panel_log(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True)
        tk.Frame(frame, bg=COLOR_TEXTO_SUAVE, height=2).pack(fill="x")

        tk.Label(
            frame, text="📋  REGISTRO DE EVENTOS",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE, pady=8
        ).pack()

        self.log_text = tk.Text(
            frame,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
            font=FUENTE_PEQUEÑA,
            relief="flat", bd=0,
            state="disabled",
            wrap="word",
            height=10
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        scrollbar = tk.Scrollbar(frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    # ── Acciones ─────────────────────────────────────────────

    def _accion_estudiantes(self):
        VentanaOla(self, self._procesar_ola)

    def _procesar_ola(self, cantidad: int):
        estudiantes = self._generar_estudiantes(cantidad)
        self.sistema.procesar_ola_de_estudiantes(estudiantes)
        self._actualizar_vista()

    def _accion_fallo(self):
        VentanaFallo(self, self.sistema.servidores, self._aplicar_fallo)

    def _aplicar_fallo(self, tipo: TipoFallo, servidor_id):
        self.sistema.simular_fallo(tipo, servidor_id)
        self._actualizar_vista()

    def _accion_reparar(self):
        caidos = [s for s in self.sistema.servidores if s.estado == EstadoServidor.CAIDO]
        if not caidos:
            messagebox.showinfo(
                "Sin servidores caídos",
                "✅  ¡Todos tus servidores están funcionando!\n\nNo hay nada que reparar ahora mismo."
            )
            return
        VentanaReparar(self, caidos, self._reparar_servidor)

    def _reparar_servidor(self, servidor_id: int):
        self.sistema.recuperar_servidor(servidor_id)
        self._actualizar_vista()

    def _accion_cola(self):
        if not self.sistema.cola_espera:
            messagebox.showinfo(
                "Cola vacía",
                "✅  La cola de espera está vacía.\n\nTodos los estudiantes ya fueron atendidos."
            )
            return
        VentanaCola(self, len(self.sistema.cola_espera), self._procesar_cola)

    def _procesar_cola(self, cantidad: int):
        self.sistema.procesar_cola_espera(cantidad)
        self._actualizar_vista()

    # ── Actualizar vista ──────────────────────────────────────

    def _actualizar_vista(self):
        self._actualizar_servidores()
        self._actualizar_metricas()
        self._actualizar_log()

    def _actualizar_servidores(self):
        for widget in self.frame_servidores_interno.winfo_children():
            widget.destroy()

        for srv in self.sistema.servidores:
            f = tk.Frame(self.frame_servidores_interno, bg=COLOR_BOTON)
            f.pack(fill="x", pady=3)

            # Color según estado
            if srv.estado == EstadoServidor.ACTIVO:
                color_estado = COLOR_VERDE
            elif srv.estado == EstadoServidor.SATURADO:
                color_estado = COLOR_AMARILLO
            else:
                color_estado = COLOR_ROJO

            tk.Label(
                f,
                text=f"{srv.estado.value}  Servidor #{srv.id}",
                font=FUENTE_SUBTIT,
                bg=COLOR_BOTON, fg=color_estado
            ).pack(side="left", padx=10, pady=6)

            # Barra de carga
            pct = srv.peticiones_actuales / srv.capacidad_maxima if srv.capacidad_maxima else 0
            barra_frame = tk.Frame(f, bg=COLOR_BORDE, height=12, width=150)
            barra_frame.pack(side="left", padx=10)
            barra_frame.pack_propagate(False)

            relleno_w = int(150 * pct)
            if relleno_w > 0:
                color_barra = COLOR_VERDE if pct < 0.6 else (COLOR_AMARILLO if pct < 0.85 else COLOR_ROJO)
                tk.Frame(barra_frame, bg=color_barra, height=12, width=relleno_w).place(x=0, y=0)

            tk.Label(
                f,
                text=f"{srv.peticiones_actuales}/{srv.capacidad_maxima}",
                font=FUENTE_PEQUEÑA,
                bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE
            ).pack(side="left", padx=6)

            tk.Label(
                f,
                text=f"Procesadas: {srv.peticiones_procesadas}",
                font=FUENTE_PEQUEÑA,
                bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE
            ).pack(side="right", padx=10)

    def _actualizar_metricas(self):
        redir  = self.sistema.balanceador.peticiones_redirigidas
        rechaz = self.sistema.balanceador.peticiones_rechazadas
        total  = redir + rechaz
        tasa   = (redir / total * 100) if total > 0 else 0

        self.lbl_sesiones.configure(
            text=str(self.sistema.gestor_sesiones.total_sesiones())
        )
        self.lbl_cola.configure(text=str(len(self.sistema.cola_espera)))
        self.lbl_atendidas.configure(text=str(redir))
        self.lbl_rechazadas.configure(text=str(rechaz))
        self.lbl_tasa.configure(
            text=f"{tasa:.1f}%",
            fg=COLOR_VERDE if tasa >= 80 else (COLOR_AMARILLO if tasa >= 50 else COLOR_ROJO)
        )

    def _actualizar_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for evento in self.sistema.log_eventos[-30:]:
            self.log_text.insert("end", evento + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _generar_estudiantes(self, cantidad: int) -> List[Estudiante]:
        grupo = []
        for _ in range(cantidad):
            nombre = random.choice(NOMBRES) + f" #{self.contador_id}"
            prioridad = 2 if random.random() < 0.1 else 1
            grupo.append(Estudiante(
                id=self.contador_id,
                nombre=nombre,
                prioridad=prioridad
            ))
            self.contador_id += 1
        return grupo


# ─────────────────────────────────────────────
#  VENTANAS EMERGENTES (diálogos de acción)
# ─────────────────────────────────────────────

class VentanaBase(tk.Toplevel):
    def __init__(self, parent, titulo: str):
        super().__init__(parent)
        self.title(titulo)
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)
        self.grab_set()  # modal

        tk.Frame(self, bg=COLOR_ACENTO, height=3).pack(fill="x")
        tk.Label(
            self, text=titulo,
            font=FUENTE_SUBTIT,
            bg=COLOR_FONDO, fg=COLOR_ACENTO,
            pady=12
        ).pack()
        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x")


class VentanaOla(VentanaBase):
    def __init__(self, parent, al_confirmar):
        super().__init__(parent, "📥  ENVIAR OLA DE ESTUDIANTES")
        self.al_confirmar = al_confirmar

        tk.Label(
            self,
            text=(
                "Simula que llegan estudiantes al portal al mismo tiempo.\n"
                "¿Cuántos estudiantes intentan conectarse ahora?"
            ),
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            justify="center", pady=10
        ).pack()

        self.var = tk.IntVar(value=50)
        self.lbl_val = tk.Label(
            self, text="50 estudiantes",
            font=("Courier New", 20, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        )
        self.lbl_val.pack()

        tk.Scale(
            self, from_=1, to=500,
            orient="horizontal",
            variable=self.var,
            command=self._actualizar,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
            troughcolor=COLOR_BORDE,
            highlightthickness=0,
            activebackground=COLOR_ACENTO,
            length=300
        ).pack(padx=30, pady=10)

        tips = [
            "💡  Empieza con 50 para ver cómo responde tu sistema.",
            "⚠️  300+ estudiantes simula la hora pico de las 08:00 AM.",
        ]
        for t in tips:
            tk.Label(self, text=t, font=FUENTE_PEQUEÑA,
                     bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE).pack()

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", pady=10)

        BotonJuego(self, "✅  ENVIAR ESTUDIANTES", self._confirmar,
                   color_acento=COLOR_VERDE).pack(pady=10)

    def _actualizar(self, val):
        self.lbl_val.configure(text=f"{val} estudiantes")

    def _confirmar(self):
        self.al_confirmar(self.var.get())
        self.destroy()


class VentanaFallo(VentanaBase):
    def __init__(self, parent, servidores, al_confirmar):
        super().__init__(parent, "💥  SIMULAR UN FALLO")
        self.servidores   = servidores
        self.al_confirmar = al_confirmar
        self.var_tipo     = tk.StringVar(value="1")
        self.var_srv      = tk.StringVar(value="0")

        tk.Label(
            self,
            text="Pon a prueba la resiliencia de tu infraestructura.",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            justify="center", pady=10
        ).pack()

        # Tipo de fallo
        tk.Label(self, text="Tipo de fallo:", font=FUENTE_SUBTIT,
                 bg=COLOR_FONDO, fg=COLOR_ROJO).pack(anchor="w", padx=20)

        tipos = [
            ("1", "⚡ Sobrecarga"),
            ("2", "🔩 Hardware"),
            ("3", "🐛 Software"),
            ("4", "🦠 Ciberataque (DDoS)"),
        ]
        for val, texto in tipos:
            tk.Radiobutton(
                self, text=texto, variable=self.var_tipo, value=val,
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                selectcolor=COLOR_BORDE, activebackground=COLOR_FONDO,
                activeforeground=COLOR_ROJO
            ).pack(anchor="w", padx=40)

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        # Servidor objetivo
        tk.Label(self, text="¿En qué servidor?", font=FUENTE_SUBTIT,
                 bg=COLOR_FONDO, fg=COLOR_ROJO).pack(anchor="w", padx=20)

        tk.Radiobutton(
            self, text="🎲 Fallo aleatorio (el sistema decide)",
            variable=self.var_srv, value="0",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            selectcolor=COLOR_BORDE, activebackground=COLOR_FONDO
        ).pack(anchor="w", padx=40)

        for srv in servidores:
            tk.Radiobutton(
                self,
                text=f"Servidor #{srv.id}  —  {srv.estado.value}",
                variable=self.var_srv, value=str(srv.id),
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                selectcolor=COLOR_BORDE, activebackground=COLOR_FONDO
            ).pack(anchor="w", padx=40)

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        BotonJuego(self, "💥  APLICAR FALLO", self._confirmar,
                   color_acento=COLOR_ROJO).pack(pady=10)

    def _confirmar(self):
        tipo_map = {
            "1": TipoFallo.SOBRECARGA,
            "2": TipoFallo.HARDWARE,
            "3": TipoFallo.SOFTWARE,
            "4": TipoFallo.CIBERATAQUE
        }
        srv_id = None if self.var_srv.get() == "0" else int(self.var_srv.get())
        self.al_confirmar(tipo_map[self.var_tipo.get()], srv_id)
        self.destroy()


class VentanaReparar(VentanaBase):
    def __init__(self, parent, caidos, al_confirmar):
        super().__init__(parent, "🔧  REPARAR SERVIDOR")
        self.al_confirmar = al_confirmar
        self.var = tk.StringVar(value=str(caidos[0].id))

        tk.Label(
            self,
            text="Selecciona el servidor que deseas recuperar:",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            pady=10
        ).pack()

        for srv in caidos:
            tk.Radiobutton(
                self,
                text=f"🔴  Servidor #{srv.id}",
                variable=self.var, value=str(srv.id),
                font=FUENTE_SUBTIT, bg=COLOR_FONDO, fg=COLOR_ROJO,
                selectcolor=COLOR_BORDE, activebackground=COLOR_FONDO
            ).pack(anchor="w", padx=40, pady=4)

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        BotonJuego(self, "🔧  REPARAR", self._confirmar,
                   color_acento=COLOR_VERDE).pack(pady=10)

    def _confirmar(self):
        self.al_confirmar(int(self.var.get()))
        self.destroy()


class VentanaCola(VentanaBase):
    def __init__(self, parent, total_espera: int, al_confirmar):
        super().__init__(parent, "♻️  ATENDER COLA DE ESPERA")
        self.al_confirmar = al_confirmar

        tk.Label(
            self,
            text=f"Hay {total_espera} estudiantes esperando.\n¿Cuántos intentas atender ahora?",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            justify="center", pady=10
        ).pack()

        self.var = tk.IntVar(value=min(50, total_espera))
        self.lbl_val = tk.Label(
            self, text=f"{min(50, total_espera)} estudiantes",
            font=("Courier New", 20, "bold"),
            bg=COLOR_FONDO, fg=COLOR_AMARILLO
        )
        self.lbl_val.pack()

        tk.Scale(
            self, from_=1, to=total_espera,
            orient="horizontal",
            variable=self.var,
            command=self._actualizar,
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
            troughcolor=COLOR_BORDE,
            highlightthickness=0,
            activebackground=COLOR_AMARILLO,
            length=300
        ).pack(padx=30, pady=10)

        tk.Frame(self, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        BotonJuego(self, "♻️  ATENDER", self._confirmar,
                   color_acento=COLOR_AMARILLO).pack(pady=10)

    def _actualizar(self, val):
        self.lbl_val.configure(text=f"{val} estudiantes")

    def _confirmar(self):
        self.al_confirmar(self.var.get())
        self.destroy()


# ─────────────────────────────────────────────
#  PANTALLA: Resultados finales
# ─────────────────────────────────────────────

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

        if tasa >= 95 and caidos == 0:
            calificacion = "🏆  INFRAESTRUCTURA PERFECTA"
            color_cal    = COLOR_VERDE
            emoji_grande = "🏆"
        elif tasa >= 80:
            calificacion = "🥇  MUY BUENA"
            color_cal    = COLOR_VERDE
            emoji_grande = "🥇"
        elif tasa >= 60:
            calificacion = "🥈  ACEPTABLE"
            color_cal    = COLOR_AMARILLO
            emoji_grande = "🥈"
        elif tasa >= 40:
            calificacion = "🥉  DEFICIENTE"
            color_cal    = COLOR_ROJO
            emoji_grande = "🥉"
        else:
            calificacion = "💀  COLAPSO TOTAL"
            color_cal    = COLOR_ROJO
            emoji_grande = "💀"

        tk.Frame(self, bg=color_cal, height=4).pack(fill="x")

        tk.Label(
            self, text=emoji_grande,
            font=("Courier New", 48),
            bg=COLOR_FONDO, fg=color_cal
        ).pack(pady=(20, 0))

        tk.Label(
            self, text="RESULTADO FINAL",
            font=("Courier New", 12),
            bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
        ).pack()

        tk.Label(
            self, text=calificacion,
            font=("Courier New", 20, "bold"),
            bg=COLOR_FONDO, fg=color_cal
        ).pack(pady=(4, 20))

        # Estadísticas
        stats_frame = tk.Frame(self, bg=COLOR_PANEL)
        stats_frame.pack(padx=60, pady=10, fill="x")
        tk.Frame(stats_frame, bg=color_cal, height=2).pack(fill="x")

        tk.Label(
            stats_frame, text="📊  RESUMEN DE TU SIMULACIÓN",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=10
        ).pack()

        datos = [
            ("Servidores desplegados",  str(len(self.sistema.servidores)),  COLOR_TEXTO),
            ("Servidores caídos al final", str(caidos),                     COLOR_ROJO if caidos > 0 else COLOR_VERDE),
            ("Algoritmo utilizado",     self.sistema.balanceador.algoritmo.value, COLOR_ACENTO),
            ("Total de peticiones",     str(total),                          COLOR_TEXTO),
            ("Estudiantes atendidos",   f"{redir}  ({tasa:.1f}%)",          COLOR_VERDE if tasa >= 80 else COLOR_AMARILLO),
            ("Estudiantes rechazados",  str(rechaz),                         COLOR_ROJO if rechaz > 0 else COLOR_VERDE),
            ("Aún en cola de espera",   str(len(self.sistema.cola_espera)), COLOR_AMARILLO),
        ]

        for etiqueta, valor, color in datos:
            fila = tk.Frame(stats_frame, bg=COLOR_PANEL)
            fila.pack(fill="x", padx=20, pady=2)
            tk.Label(fila, text=etiqueta + ":", font=FUENTE_NORMAL,
                     bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE, width=28, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, font=FUENTE_SUBTIT,
                     bg=COLOR_PANEL, fg=color).pack(side="left")

        tk.Frame(stats_frame, bg=COLOR_BORDE, height=1).pack(fill="x", pady=8)

        # Conclusiones
        tk.Label(
            stats_frame, text="💡  LO QUE APRENDISTE HOY",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=6
        ).pack()

        conclusiones = [
            "• Un solo servidor no aguanta miles de peticiones simultáneas.",
            "• El balanceador de carga evita que un servidor colapse solo.",
            "• Los tokens de sesión protegen a los estudiantes si hay fallos.",
            "• La alta disponibilidad requiere redundancia: si uno cae, otros cubren.",
        ]
        for c in conclusiones:
            tk.Label(
                stats_frame, text=c, font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO, anchor="w"
            ).pack(fill="x", padx=20, pady=1)

        tk.Frame(stats_frame, bg=color_cal, height=2).pack(fill="x", pady=(10, 0))

        BotonJuego(self, "🚪  SALIR DEL JUEGO", self.al_salir,
                   color_acento=COLOR_TEXTO_SUAVE).pack(pady=20)


# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────

class Aplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎓 Simulador de Matrículas Universitarias")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLOR_FONDO)
        self.sistema: Optional[SistemaDeMatricula] = None
        self._pantalla_actual = None

    def iniciar(self):
        self._mostrar_bienvenida()
        self.root.mainloop()

    def _limpiar(self):
        if self._pantalla_actual:
            self._pantalla_actual.destroy()

    def _mostrar_bienvenida(self):
        self._limpiar()
        self._pantalla_actual = PantallaBienvenida(self.root, self._mostrar_configuracion)
        self._pantalla_actual.pack(fill="both", expand=True)

    def _mostrar_configuracion(self):
        self._limpiar()
        self._pantalla_actual = PantallaConfiguracion(self.root, self._iniciar_juego)
        self._pantalla_actual.pack(fill="both", expand=True)

    def _iniciar_juego(self, num_servidores: int, capacidad: int, algoritmo: AlgoritmoBalanceo):
        self.sistema = SistemaDeMatricula(num_servidores, capacidad, algoritmo)
        self._limpiar()
        self._pantalla_actual = PantallaJuego(
            self.root, self.sistema, self._mostrar_resultados
        )
        self._pantalla_actual.pack(fill="both", expand=True)

    def _mostrar_resultados(self):
        self._limpiar()
        self._pantalla_actual = PantallaResultados(
            self.root, self.sistema, self.root.quit
        )
        self._pantalla_actual.pack(fill="both", expand=True)