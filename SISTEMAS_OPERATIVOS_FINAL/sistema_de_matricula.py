# ============================================================
#  sistema_de_matricula.py
#  Orquestador central con motor de Victoria/Derrota y Misiones
# ============================================================

import random
from typing import List, Optional
from estados import AlgoritmoBalanceo, EstadoServidor, TipoFallo
from estudiante import Estudiante
from servidor_web import ServidorWeb
from balanceador_de_carga import BalanceadorDeCarga
from gestor_de_sesiones import GestorDeSesiones


class GestorDeMisiones:
    def __init__(self, activo: bool = False):
        self.activo = activo
        self.mision_actual = 1 if activo else 0
        self.textos = {
            1: "💡 MISIÓN 1: Envía una ola de estudiantes para llenar los servidores.",
            2: "💡 MISIÓN 2: Provoca un fallo en uno de tus servidores.",
            3: "💡 MISIÓN 3: Repara el servidor caído para restaurar la red.",
            4: "💡 MISIÓN 4: Despacha los estudiantes retenidos en la cola.",
            5: "✅ ¡TUTORIAL COMPLETADO! Revisa tus Resultados Finales.",
        }
        self.sugerencias = {
            1: "💡 Tip: Envía estudiantes para ver cómo se distribuye la carga.",
            2: "💡 Tip: Prueba provocar un fallo para ver la resiliencia del sistema.",
            3: "💡 Tip: Si hay servidores caídos, repáralos para recuperar capacidad.",
            4: "💡 Tip: Atiende la cola de espera para que nadie se quede sin matricularse.",
        }
        # Registro de qué pasos ya fueron completados (para modo libre)
        self.completados = set()

    def instruccion(self) -> str:
        if not self.activo:
            return ""
        return self.textos.get(self.mision_actual, "")

    def sugerencia_libre(self, paso: int) -> str:
        """Devuelve una sugerencia no bloqueante para modo libre."""
        return self.sugerencias.get(paso, "")

    def avanzar(self, paso: int):
        """
        En modo guiado: avanza solo si es el paso correcto.
        En modo libre: registra el paso como completado.
        """
        if self.activo:
            if self.mision_actual == paso:
                self.mision_actual += 1
        else:
            self.completados.add(paso)

    def completado(self) -> bool:
        return self.mision_actual >= 5

    def habilitado(self, paso: int) -> bool:
        """Solo bloquea en modo guiado."""
        if not self.activo:
            return True
        return self.mision_actual == paso or self.completado()

    def forzar_avance(self):
        """
        Fuerza avanzar la misión actual en modo guiado.
        Usado para desbloquear cuando el estado ya cumple la condición.
        """
        if self.activo and not self.completado():
            self.mision_actual += 1


class SistemaDeMatricula:
    def __init__(
        self,
        num_servidores: int,
        capacidad_por_servidor: int,
        algoritmo: AlgoritmoBalanceo,
        modo_misiones: bool = False
    ):
        self.servidores: List[ServidorWeb] = [
            ServidorWeb(id=i + 1, capacidad_maxima=capacidad_por_servidor)
            for i in range(num_servidores)
        ]
        self.balanceador      = BalanceadorDeCarga(algoritmo)
        self.gestor_sesiones  = GestorDeSesiones()
        self.gestor_misiones  = GestorDeMisiones(modo_misiones)

        self.cola_espera: List[Estudiante] = []
        self.log_eventos: List[str]        = []
        self.ronda       = 0
        self.estado_juego = "EN_CURSO"
        self.meta_estudiantes = 300

    def registrar_evento(self, mensaje: str):
        self.log_eventos.append(f"  [Ronda {self.ronda}] {mensaje}")

    # ── Acciones principales ──────────────────────────────────

    def procesar_ola_de_estudiantes(self, estudiantes: List[Estudiante]):
        if self.estado_juego != "EN_CURSO":
            return
        self.ronda += 1
        self.registrar_evento(f"⚡ Llegan {len(estudiantes)} estudiantes al portal.")

        for estudiante in estudiantes:
            estudiante.intentos += 1
            servidor = self.balanceador.asignar(self.servidores, estudiante)
            if servidor:
                token = self.gestor_sesiones.iniciar_sesion(estudiante)
                self.registrar_evento(
                    f"🟢 {estudiante.nombre} → Servidor #{servidor.id} | Token: {token}"
                )
            else:
                self.cola_espera.append(estudiante)
                self.registrar_evento(
                    f"🟡 {estudiante.nombre} → Sin servidor, va a cola."
                )

        self.gestor_misiones.avanzar(1)
        self.evaluar_condiciones()

    def simular_fallo(self, tipo: TipoFallo, servidor_id: Optional[int] = None):
        if self.estado_juego != "EN_CURSO":
            return
        self.ronda += 1

        if servidor_id is not None:
            objetivo = next((s for s in self.servidores if s.id == servidor_id), None)
            if objetivo:
                objetivo.aplicar_fallo()
        else:
            activos = [s for s in self.servidores if s.estado != EstadoServidor.CAIDO]
            if activos:
                random.choice(activos).aplicar_fallo()

        self.registrar_evento(f"🔴 FALLO [{tipo.value}] detectado en el sistema.")
        self.gestor_misiones.avanzar(2)
        self.evaluar_condiciones()

    def recuperar_servidor(self, servidor_id: int):
        servidor = next((s for s in self.servidores if s.id == servidor_id), None)
        if servidor:
            servidor.recuperar()
            self.registrar_evento(f"🔧 Servidor #{servidor_id} recuperado y vuelto a línea.")

        # Avanzar misión 3 al reparar
        self.gestor_misiones.avanzar(3)

        # Seguridad: si no quedan servidores caídos y estamos en misión 3, forzar avance
        caidos = [s for s in self.servidores if s.estado == EstadoServidor.CAIDO]
        if not caidos and self.gestor_misiones.activo and self.gestor_misiones.mision_actual == 3:
            self.gestor_misiones.forzar_avance()

    def procesar_cola_espera(self, cantidad: int = 10):
        if self.estado_juego != "EN_CURSO":
            return
        self.ronda += 1
        procesados = 0
        aun_en_espera = []

        for estudiante in self.cola_espera:
            if procesados >= cantidad:
                aun_en_espera.append(estudiante)
                continue
            servidor = self.balanceador.asignar(self.servidores, estudiante)
            if servidor:
                self.gestor_sesiones.iniciar_sesion(estudiante)
                procesados += 1
            else:
                aun_en_espera.append(estudiante)

        self.cola_espera = aun_en_espera
        self.registrar_evento(
            f"📤 Cola procesada: {procesados} atendidos, {len(self.cola_espera)} esperando."
        )
        self.gestor_misiones.avanzar(4)
        self.evaluar_condiciones()

    # ── Motor de victoria/derrota ─────────────────────────────

    def evaluar_condiciones(self):
        # En modo tutorial la victoria la declara la GUI al completar misiones
        if self.gestor_misiones.activo:
            return

        redirigidas = self.balanceador.peticiones_redirigidas
        rechazadas  = self.balanceador.peticiones_rechazadas
        total       = redirigidas + rechazadas
        tasa        = (redirigidas / total * 100) if total > 0 else 100
        activos     = sum(1 for s in self.servidores if s.estado != EstadoServidor.CAIDO)

        if activos == 0 or (total > 100 and tasa < 40):
            self.estado_juego = "DERROTA"
        elif redirigidas >= self.meta_estudiantes:
            self.estado_juego = "VICTORIA"