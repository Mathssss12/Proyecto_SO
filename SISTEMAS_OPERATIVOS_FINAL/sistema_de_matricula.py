# ============================================================
#  sistema_de_matricula.py
#  Orquestador central: coordina servidores, balanceador
#  y gestor de sesiones
# ============================================================

import random
from typing import List, Optional
from estados import AlgoritmoBalanceo, EstadoServidor, TipoFallo
from estudiante import Estudiante
from servidor_web import ServidorWeb
from balanceador_de_carga import BalanceadorDeCarga
from gestor_de_sesiones import GestorDeSesiones


class SistemaDeMatricula:
    def __init__(
        self,
        num_servidores: int,
        capacidad_por_servidor: int,
        algoritmo: AlgoritmoBalanceo
    ):
        self.servidores: List[ServidorWeb] = [
            ServidorWeb(id=i + 1, capacidad_maxima=capacidad_por_servidor)
            for i in range(num_servidores)
        ]
        self.balanceador = BalanceadorDeCarga(algoritmo)
        self.gestor_sesiones = GestorDeSesiones()
        self.cola_espera: List[Estudiante] = []
        self.log_eventos: List[str] = []
        self.ronda = 0

    def registrar_evento(self, mensaje: str):
        self.log_eventos.append(f"  [Ronda {self.ronda}] {mensaje}")

    def procesar_ola_de_estudiantes(self, estudiantes: List[Estudiante]):
        self.ronda += 1
        self.registrar_evento(f"⚡ Llegan {len(estudiantes)} estudiantes al portal.")

        for estudiante in estudiantes:
            estudiante.intentos += 1
            servidor = self.balanceador.asignar(self.servidores, estudiante)

            if servidor:
                token = self.gestor_sesiones.iniciar_sesion(estudiante)
                self.registrar_evento(
                    f" {estudiante.nombre} → Servidor #{servidor.id} | Token: {token}"
                )
            else:
                self.cola_espera.append(estudiante)
                self.registrar_evento(
                    f" {estudiante.nombre} → Sin servidor disponible, va a cola de espera."
                )

    def simular_fallo(self, tipo: TipoFallo, servidor_id: Optional[int] = None):
        self.ronda += 1

        if servidor_id is not None:
            objetivo = next((s for s in self.servidores if s.id == servidor_id), None)
            if objetivo:
                objetivo.aplicar_fallo()
                self.registrar_evento(
                    f" FALLO [{tipo.value}] aplicado al Servidor #{servidor_id}"
                )
        else:
            activos = [s for s in self.servidores if s.estado != EstadoServidor.CAIDO]
            if activos:
                victima = random.choice(activos)
                victima.aplicar_fallo()
                self.registrar_evento(
                    f" FALLO ALEATORIO [{tipo.value}] → Servidor #{victima.id} caído"
                )

    def recuperar_servidor(self, servidor_id: int):
        servidor = next((s for s in self.servidores if s.id == servidor_id), None)
        if servidor:
            servidor.recuperar()
            self.registrar_evento(f"  Servidor #{servidor_id} recuperado y vuelto a línea.")

    def procesar_cola_espera(self, cantidad: int = 10):
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
                self.registrar_evento(
                    f"♻️  {estudiante.nombre} salió de cola → Servidor #{servidor.id}"
                )
                procesados += 1
            else:
                aun_en_espera.append(estudiante)

        self.cola_espera = aun_en_espera
        self.registrar_evento(
            f"📤 Cola procesada: {procesados} atendidos, "
            f"{len(self.cola_espera)} aún esperando."
        )

    def estado_actual(self):
        print("\n" + "═" * 65)
        print("  ESTADO ACTUAL DEL SISTEMA")
        print("═" * 65)
        print(f"  Algoritmo de balanceo : {self.balanceador.algoritmo.value}")
        print(f"  Sesiones activas      : {self.gestor_sesiones.total_sesiones()}")
        print(f"  En cola de espera     : {len(self.cola_espera)}")
        print(f"  Peticiones redirigidas: {self.balanceador.peticiones_redirigidas}")
        print(f"  Peticiones rechazadas : {self.balanceador.peticiones_rechazadas}")
        print()
        print("  🖥️  SERVIDORES:")
        for servidor in self.servidores:
            print(servidor)
        print("═" * 65)

    def mostrar_log(self, ultimos: int = 10):
        print("\n" + "─" * 65)
        print(f"  ÚLTIMOS {ultimos} EVENTOS:")
        print("─" * 65)
        for evento in self.log_eventos[-ultimos:]:
            print(evento)
        print("─" * 65)