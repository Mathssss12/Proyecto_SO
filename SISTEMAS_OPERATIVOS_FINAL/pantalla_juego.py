# ============================================================
#  pantalla_juego.py
#  Pantalla principal del juego: servidores, métricas y acciones
# ============================================================

import tkinter as tk
import random
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_AMARILLO,
    COLOR_ROJO, COLOR_VERDE, COLOR_BORDE, COLOR_TEXTO,
    COLOR_TEXTO_SUAVE, COLOR_BOTON,
    FUENTE_TITULO, FUENTE_SUBTIT, FUENTE_NORMAL, FUENTE_PEQUEÑA,
    NOMBRES
)
from componentes import BotonJuego, PanelModalInterno
from estados import EstadoServidor, TipoFallo
from estudiante import Estudiante
from sistema_de_matricula import SistemaDeMatricula


class PantallaJuego(tk.Frame):
    def __init__(self, parent, sistema: SistemaDeMatricula, al_finalizar):
        super().__init__(parent, bg=COLOR_FONDO)
        self.sistema      = sistema
        self.al_finalizar = al_finalizar
        self.contador_id  = 1
        self.modal_activo = None
        self._construir()
        self._actualizar_vista()

    # ── Construcción de la pantalla ───────────────────────────

    def _construir(self):
        # Cabecera
        cabecera = tk.Frame(self, bg=COLOR_PANEL)
        cabecera.pack(fill="x")
        tk.Frame(cabecera, bg=COLOR_ACENTO, height=3).pack(fill="x")

        cont_cab = tk.Frame(cabecera, bg=COLOR_PANEL)
        cont_cab.pack(fill="x", padx=20)

        tk.Label(
            cont_cab,
            text="🎓  PORTAL DE MATRÍCULAS — SALA DE CONTROL",
            font=FUENTE_TITULO, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=10
        ).pack(side="left", expand=True, anchor="center", padx=(50, 0))

        tk.Button(
            cont_cab, text="?",
            font=("Courier New", 12, "bold"),
            bg=COLOR_BOTON, fg=COLOR_AMARILLO,
            activebackground=COLOR_BOTON, activeforeground=COLOR_AMARILLO,
            relief="flat", bd=0, width=3, height=1,
            cursor="hand2", command=self._mostrar_ayuda
        ).pack(side="right", padx=10, pady=10)

        # Banner: modo guiado muestra misión, modo libre muestra sugerencia
        if self.sistema.gestor_misiones.activo:
            self.lbl_mision = tk.Label(
                self, text="",
                font=FUENTE_SUBTIT,
                bg=COLOR_VERDE, fg=COLOR_FONDO, pady=5
            )
            self.lbl_mision.pack(fill="x")
        else:
            self.lbl_sugerencia = tk.Label(
                self,
                text="👆 Comienza enviando una ola de estudiantes.",
                font=FUENTE_PEQUEÑA,
                bg=COLOR_BORDE, fg=COLOR_TEXTO, pady=5
            )
            self.lbl_sugerencia.pack(fill="x")

        # Cuerpo principal
        cuerpo = tk.Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)

        izq = tk.Frame(cuerpo, bg=COLOR_FONDO)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self._panel_servidores(izq)
        self._panel_metricas(izq)

        der = tk.Frame(cuerpo, bg=COLOR_FONDO)
        der.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self._panel_acciones(der)
        self._panel_log(der)

    # ── Paneles ───────────────────────────────────────────────

    def _panel_servidores(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_ACENTO, height=2).pack(fill="x")
        tk.Label(
            frame, text="ESTADO DE TUS SERVIDORES",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_ACENTO, pady=8
        ).pack()
        self.frame_servidores_interno = tk.Frame(frame, bg=COLOR_PANEL)
        self.frame_servidores_interno.pack(fill="x", padx=10, pady=(0, 10))

    def _panel_metricas(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_VERDE, height=2).pack(fill="x")
        tk.Label(
            frame, text="MÉTRICAS EN TIEMPO REAL",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_VERDE, pady=8
        ).pack()

        grid = tk.Frame(frame, bg=COLOR_PANEL)
        grid.pack(fill="x", padx=10, pady=(0, 10))

        self.lbl_sesiones   = self._metrica(grid, "Sesiones activas", "0", COLOR_VERDE,    0)
        self.lbl_cola       = self._metrica(grid, "En cola",          "0", COLOR_AMARILLO, 1)
        self.lbl_atendidas  = self._metrica(grid, "Atendidas",        "0", COLOR_ACENTO,   2)
        self.lbl_rechazadas = self._metrica(grid, "Rechazadas",       "0", COLOR_ROJO,     3)
        self.lbl_tasa       = self._metrica(grid, "Tasa Éxito",       "—", COLOR_VERDE,    4)

    def _metrica(self, parent, etiqueta, valor, color, col):
        f = tk.Frame(parent, bg=COLOR_BOTON)
        f.grid(row=0, column=col, padx=4, pady=4, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        lbl = tk.Label(f, text=valor, font=("Courier New", 18, "bold"), bg=COLOR_BOTON, fg=color)
        lbl.pack(pady=(8, 0))
        tk.Label(f, text=etiqueta, font=FUENTE_PEQUEÑA, bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE).pack(pady=(0, 8))
        return lbl

    def _panel_acciones(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="x", pady=(0, 8))
        tk.Frame(frame, bg=COLOR_AMARILLO, height=2).pack(fill="x")
        tk.Label(
            frame, text="ACCIONES DISPONIBLES",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_AMARILLO, pady=8
        ).pack()

        self.btn_ola   = self._boton_accion(frame, "Enviar ola de estudiantes", "Simula que llegan estudiantes al portal.",  self._accion_estudiantes, COLOR_ACENTO)
        self.btn_fallo = self._boton_accion(frame, "Provocar un fallo",          "Simula un fallo inesperado en hardware.",   self._accion_fallo,       COLOR_ROJO)
        self.btn_rep   = self._boton_accion(frame, "Reparar servidor caído",     "Vuelve a poner en línea un servidor.",      self._accion_reparar,     COLOR_VERDE)
        self.btn_cola  = self._boton_accion(frame, "Atender cola de espera",     "Reintenta conectar a los retenidos.",       self._accion_cola,        COLOR_AMARILLO)
        self.btn_fin   = self._boton_accion(frame, "Ver Resultados Finales",     "Termina la simulación y calcula nota.",     self.al_finalizar,        COLOR_TEXTO_SUAVE)

    def _boton_accion(self, parent, texto, tooltip, comando, color):
        f = tk.Frame(parent, bg=COLOR_BOTON)
        f.pack(fill="x", padx=10, pady=3)
        btn = BotonJuego(f, texto=texto, comando=comando, color_acento=color)
        btn.pack(side="left", padx=(0, 8))
        tk.Label(
            f, text=tooltip, font=FUENTE_PEQUEÑA,
            bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE, justify="left"
        ).pack(side="left", pady=6)
        return btn

    def _panel_log(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL)
        frame.pack(fill="both", expand=True)
        tk.Frame(frame, bg=COLOR_TEXTO_SUAVE, height=2).pack(fill="x")
        tk.Label(
            frame, text="REGISTRO DE EVENTOS",
            font=FUENTE_SUBTIT, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE, pady=8
        ).pack()
        self.log_text = tk.Text(
            frame, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            font=FUENTE_PEQUEÑA, relief="flat", bd=0,
            state="disabled", wrap="word", height=10
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # ── Ayuda ─────────────────────────────────────────────────

    def _mostrar_ayuda(self):
        self._destruir_modal()
        modal = PanelModalInterno(self, "GUÍA DEL SISTEMA OPERATIVO", COLOR_AMARILLO, width=650, height=520)
        self.modal_activo = modal

        tk.Button(
            modal.cabecera, text="×",
            font=("Courier New", 16, "bold"),
            bg=COLOR_PANEL, fg=COLOR_ROJO,
            bd=0, cursor="hand2", command=self._destruir_modal
        ).pack(side="right", padx=15, pady=5)

        guia = (
            "1. ESTADO DE LOS SERVIDORES:\n"
            "   Muestra la carga actual de cada nodo en tiempo real.\n"
            "   IMPORTANCIA: Previene la saturación grupal. Si ves\n"
            "   barras rojas, la infraestructura está en estado crítico.\n\n"
            "2. ENVIAR OLA DE ESTUDIANTES:\n"
            "   Simula tráfico masivo concurrente ingresando al sistema.\n"
            "   IMPORTANCIA: Permite probar el comportamiento bajo estrés.\n\n"
            "3. PROVOCAR UN FALLO:\n"
            "   Simula un fallo inesperado en hardware o software.\n"
            "   IMPORTANCIA: Evalúa la tolerancia a fallos del sistema.\n\n"
            "4. REPARAR SERVIDOR CAÍDO:\n"
            "   Restaura un nodo caído para recuperar capacidad.\n"
            "   IMPORTANCIA: Demuestra la resiliencia de la arquitectura.\n\n"
            "5. ATENDER COLA DE ESPERA:\n"
            "   Despacha estudiantes que no pudieron conectarse.\n"
            "   IMPORTANCIA: Garantiza que nadie pierda su matrícula."
        )
        area = tk.Text(
            modal.cuerpo, bg=COLOR_PANEL, fg=COLOR_TEXTO,
            font=FUENTE_NORMAL, relief="flat", wrap="word"
        )
        area.pack(fill="both", expand=True, padx=5, pady=5)
        area.insert("1.0", guia)
        area.configure(state="disabled")

    # ── Modales de acción ─────────────────────────────────────

    def _destruir_modal(self):
        if self.modal_activo:
            self.modal_activo.destroy()
            self.modal_activo = None

    def _accion_estudiantes(self):
        self._destruir_modal()
        modal = PanelModalInterno(self, "ENVIAR OLA DE ESTUDIANTES", COLOR_ACENTO, width=500, height=350)
        self.modal_activo = modal

        tk.Label(
            modal.cuerpo,
            text="¿Cuántos estudiantes intentan conectarse ahora?",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO, pady=10
        ).pack()

        var_cantidad = tk.IntVar(value=50)
        lbl_val = tk.Label(
            modal.cuerpo, text="50 estudiantes",
            font=("Courier New", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO
        )
        lbl_val.pack()

        tk.Scale(
            modal.cuerpo, from_=1, to=500, orient="horizontal",
            variable=var_cantidad,
            command=lambda v: lbl_val.configure(text=f"{v} estudiantes"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, troughcolor=COLOR_BORDE,
            highlightthickness=0, activebackground=COLOR_ACENTO, length=320
        ).pack(pady=15)

        if not self.sistema.gestor_misiones.activo:
            tk.Label(
                modal.cuerpo,
                text="💡 Tip: Envía más de 300 para saturar los servidores y ver la cola.",
                font=FUENTE_PEQUEÑA, bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE
            ).pack()

        def ejecutar():
            estudiantes = [
                Estudiante(id=self.contador_id + i, nombre=random.choice(NOMBRES))
                for i in range(var_cantidad.get())
            ]
            self.contador_id += var_cantidad.get()
            self.sistema.procesar_ola_de_estudiantes(estudiantes)
            self._actualizar_vista()
            self._destruir_modal()

        BotonJuego(modal.cuerpo, "COMPROBAR TRÁFICO", ejecutar, color_acento=COLOR_VERDE).pack(pady=5)
        BotonJuego(modal, "CANCELAR", self._destruir_modal, color_acento=COLOR_ROJO).pack(pady=(0, 10))

    def _accion_fallo(self):
        self._destruir_modal()
        modal = PanelModalInterno(self, "SIMULAR UN FALLO DE RED", COLOR_ROJO, width=540, height=450)
        self.modal_activo = modal

        tk.Label(
            modal.cuerpo,
            text="Elige el tipo de percance y el nodo afectado:",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(pady=(0, 15))

        var_tipo = tk.StringVar(value="1")
        var_srv  = tk.StringVar(value="0")

        frame_op = tk.Frame(modal.cuerpo, bg=COLOR_FONDO)
        frame_op.pack(fill="both", expand=True, pady=5)

        f_izq = tk.Frame(frame_op, bg=COLOR_FONDO)
        f_izq.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(
            f_izq, text="Tipo de Fallo:",
            font=FUENTE_SUBTIT, bg=COLOR_FONDO, fg=COLOR_ROJO
        ).pack(anchor="w", pady=(0, 10))
        for val, txt in [("1", "Sobrecarga"), ("2", "Hardware"), ("3", "Software"), ("4", "DDoS")]:
            tk.Radiobutton(
                f_izq, text=txt, variable=var_tipo, value=val,
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                selectcolor=COLOR_PANEL, activebackground=COLOR_FONDO,
                activeforeground=COLOR_ACENTO, anchor="w"
            ).pack(fill="x", anchor="w", pady=4)

        f_der = tk.Frame(frame_op, bg=COLOR_FONDO)
        f_der.pack(side="right", fill="both", expand=True, padx=10)
        tk.Label(
            f_der, text="Dispositivo:",
            font=FUENTE_SUBTIT, bg=COLOR_FONDO, fg=COLOR_ROJO
        ).pack(anchor="w", pady=(0, 10))
        tk.Radiobutton(
            f_der, text="Aleatorio", variable=var_srv, value="0",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
            selectcolor=COLOR_PANEL, activebackground=COLOR_FONDO,
            activeforeground=COLOR_ACENTO, anchor="w"
        ).pack(fill="x", anchor="w", pady=4)
        for srv in self.sistema.servidores:
            tk.Radiobutton(
                f_der, text=f"Servidor #{srv.id}", variable=var_srv, value=str(srv.id),
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                selectcolor=COLOR_PANEL, activebackground=COLOR_FONDO,
                activeforeground=COLOR_ACENTO, anchor="w"
            ).pack(fill="x", anchor="w", pady=4)

        def ejecutar():
            t_map = {
                "1": TipoFallo.SOBRECARGA,
                "2": TipoFallo.HARDWARE,
                "3": TipoFallo.SOFTWARE,
                "4": TipoFallo.CIBERATAQUE
            }
            srv_id = None if var_srv.get() == "0" else int(var_srv.get())
            self.sistema.simular_fallo(t_map[var_tipo.get()], srv_id)
            self._actualizar_vista()
            self._destruir_modal()

        BotonJuego(modal.cuerpo, "PROVOCAR CAÍDA", ejecutar, color_acento=COLOR_ROJO).pack(pady=5)
        BotonJuego(modal.cuerpo, "RETROCEDER", self._destruir_modal, color_acento=COLOR_TEXTO_SUAVE).pack(pady=5)

    def _accion_reparar(self):
        self._destruir_modal()
        caidos = [s for s in self.sistema.servidores if s.estado == EstadoServidor.CAIDO]

        if not caidos:
            modal = PanelModalInterno(self, "SISTEMA SALUDABLE", COLOR_VERDE, width=450, height=280)
            self.modal_activo = modal
            tk.Label(
                modal.cuerpo,
                text="Todos los servidores están estables.\nNo hay anomalías.",
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center"
            ).pack(pady=10)
            if not self.sistema.gestor_misiones.activo:
                tk.Label(
                    modal.cuerpo,
                    text="💡 Tip: Provoca un fallo primero para\nluego practicar la reparación.",
                    font=FUENTE_PEQUEÑA, bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE, justify="center"
                ).pack(pady=6)
            BotonJuego(modal, "ENTENDIDO", self._destruir_modal, color_acento=COLOR_VERDE).pack(pady=10)
            return

        modal = PanelModalInterno(self, "INFRAESTRUCTURA CAÍDA", COLOR_VERDE, width=480, height=320)
        self.modal_activo = modal
        tk.Label(
            modal.cuerpo,
            text="Selecciona el nodo a levantar:",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(pady=10)

        var_srv = tk.StringVar(value=str(caidos[0].id))
        for srv in caidos:
            tk.Radiobutton(
                modal.cuerpo,
                text=f"Servidor #{srv.id}  —  CAÍDO",
                variable=var_srv, value=str(srv.id),
                font=FUENTE_SUBTIT, bg=COLOR_FONDO, fg=COLOR_ROJO,
                selectcolor=COLOR_BORDE
            ).pack(anchor="w", padx=30, pady=4)

        def ejecutar():
            self.sistema.recuperar_servidor(int(var_srv.get()))
            self._actualizar_vista()
            self._destruir_modal()

        BotonJuego(modal.cuerpo, "REINICIAR SERVICIO", ejecutar, color_acento=COLOR_VERDE).pack(pady=10)
        BotonJuego(modal, "CANCELAR", self._destruir_modal, color_acento=COLOR_ROJO).pack(pady=(0, 10))

    def _accion_cola(self):
        self._destruir_modal()

        if not self.sistema.cola_espera:
            modal = PanelModalInterno(self, "BUFFER DIRECTO", COLOR_VERDE, width=450, height=280)
            self.modal_activo = modal
            tk.Label(
                modal.cuerpo,
                text="La cola está vacía.\nNo hay solicitudes en espera.",
                font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center"
            ).pack(pady=10)
            if not self.sistema.gestor_misiones.activo:
                tk.Label(
                    modal.cuerpo,
                    text="💡 Envía más estudiantes y llena los servidores\npara generar cola de espera.",
                    font=FUENTE_PEQUEÑA, bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE, justify="center"
                ).pack(pady=6)
            BotonJuego(modal, "VOLVER", self._destruir_modal, color_acento=COLOR_VERDE).pack(pady=10)
            return

        total = len(self.sistema.cola_espera)
        modal = PanelModalInterno(self, "ATENDER BUFFER DE ESPERA", COLOR_AMARILLO, width=480, height=350)
        self.modal_activo = modal

        tk.Label(
            modal.cuerpo,
            text=f"Hay {total} solicitudes en cola.\n¿Cuántas deseas despachar?",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(pady=10)

        var_cant = tk.IntVar(value=min(50, total))
        lbl_v = tk.Label(
            modal.cuerpo, text=f"{min(50, total)} estudiantes",
            font=("Courier New", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_AMARILLO
        )
        lbl_v.pack()

        tk.Scale(
            modal.cuerpo, from_=1, to=total, orient="horizontal",
            variable=var_cant,
            command=lambda v: lbl_v.configure(text=f"{v} estudiantes"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, troughcolor=COLOR_BORDE,
            highlightthickness=0, activebackground=COLOR_AMARILLO, length=300
        ).pack(pady=10)

        def ejecutar():
            self.sistema.procesar_cola_espera(var_cant.get())
            if self.sistema.gestor_misiones.activo and self.sistema.gestor_misiones.completado():
                self.sistema.estado_juego = "VICTORIA"
            self._actualizar_vista()
            self._destruir_modal()

        BotonJuego(modal.cuerpo, "PROCESAR SOLICITUDES", ejecutar, color_acento=COLOR_AMARILLO).pack(pady=5)
        BotonJuego(modal, "CERRAR", self._destruir_modal, color_acento=COLOR_ROJO).pack(pady=(0, 10))

    # ── Actualizar vista ──────────────────────────────────────

    def _actualizar_vista(self):
        # Modo guiado: banner + bloqueo de botones
        if self.sistema.gestor_misiones.activo:
            self.lbl_mision.configure(text=self.sistema.gestor_misiones.instruccion())
            self.btn_ola.configure(   state="normal" if self.sistema.gestor_misiones.habilitado(1) else "disabled")
            self.btn_fallo.configure( state="normal" if self.sistema.gestor_misiones.habilitado(2) else "disabled")
            self.btn_rep.configure(   state="normal" if self.sistema.gestor_misiones.habilitado(3) else "disabled")
            self.btn_cola.configure(  state="normal" if self.sistema.gestor_misiones.habilitado(4) else "disabled")
            self.btn_fin.configure(   state="normal" if self.sistema.gestor_misiones.completado()  else "disabled")

        # Modo libre: sugerencia dinámica sin bloqueos
        else:
            redir  = self.sistema.balanceador.peticiones_redirigidas
            rechaz = self.sistema.balanceador.peticiones_rechazadas
            total  = redir + rechaz
            tasa   = (redir / total * 100) if total > 0 else 100
            caidos = [s for s in self.sistema.servidores if s.estado == EstadoServidor.CAIDO]

            if total == 0:
                sugerencia = "👆 Comienza enviando una ola de estudiantes."
            elif caidos:
                sugerencia = "⚠️  Hay servidores caídos. ¡Repáralos para recuperar capacidad!"
            elif self.sistema.cola_espera:
                sugerencia = f"⏳  {len(self.sistema.cola_espera)} estudiantes esperan. ¡Atiende la cola!"
            elif tasa < 70:
                sugerencia = "📉  Tasa baja. Provoca un fallo y observa cómo responde el sistema."
            else:
                sugerencia = "✅  Sistema estable. Envía más estudiantes para seguir probando."

            self.lbl_sugerencia.configure(text=sugerencia)

        # Servidores
        for widget in self.frame_servidores_interno.winfo_children():
            widget.destroy()

        for srv in self.sistema.servidores:
            f = tk.Frame(self.frame_servidores_interno, bg=COLOR_BOTON)
            f.pack(fill="x", pady=3)

            color_st = (
                COLOR_VERDE    if srv.estado == EstadoServidor.ACTIVO   else
                COLOR_AMARILLO if srv.estado == EstadoServidor.SATURADO else
                COLOR_ROJO
            )
            tk.Label(
                f, text=f"{srv.estado.value}  Servidor #{srv.id}",
                font=FUENTE_SUBTIT, bg=COLOR_BOTON, fg=color_st
            ).pack(side="left", padx=10, pady=6)

            pct = srv.peticiones_actuales / srv.capacidad_maxima if srv.capacidad_maxima else 0
            barra_f = tk.Frame(f, bg=COLOR_BORDE, height=12, width=150)
            barra_f.pack(side="left", padx=10)
            barra_f.pack_propagate(False)
            relleno_w = int(150 * pct)
            if relleno_w > 0:
                col_b = COLOR_VERDE if pct < 0.6 else (COLOR_AMARILLO if pct < 0.85 else COLOR_ROJO)
                tk.Frame(barra_f, bg=col_b, height=12, width=relleno_w).place(x=0, y=0)

            tk.Label(
                f, text=f"{srv.peticiones_actuales}/{srv.capacidad_maxima}",
                font=FUENTE_PEQUEÑA, bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE
            ).pack(side="left", padx=6)
            tk.Label(
                f, text=f"Procesadas: {srv.peticiones_procesadas}",
                font=FUENTE_PEQUEÑA, bg=COLOR_BOTON, fg=COLOR_TEXTO_SUAVE
            ).pack(side="right", padx=10)

        # Métricas
        redir  = self.sistema.balanceador.peticiones_redirigidas
        rechaz = self.sistema.balanceador.peticiones_rechazadas
        total  = redir + rechaz
        tasa   = (redir / total * 100) if total > 0 else 100

        self.lbl_sesiones.configure(text=str(self.sistema.gestor_sesiones.total_sesiones()))
        self.lbl_cola.configure(text=str(len(self.sistema.cola_espera)))
        self.lbl_atendidas.configure(text=str(redir))
        self.lbl_rechazadas.configure(text=str(rechaz))
        self.lbl_tasa.configure(
            text=f"{tasa:.1f}%",
            fg=COLOR_VERDE if tasa >= 80 else (COLOR_AMARILLO if tasa >= 50 else COLOR_ROJO)
        )

        # Log
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for ev in self.sistema.log_eventos[-30:]:
            self.log_text.insert("end", ev + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

        # Detectar fin de juego en modo libre
        if not self.sistema.gestor_misiones.activo and self.sistema.estado_juego != "EN_CURSO":
            self.after(800, self.al_finalizar)