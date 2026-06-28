# ============================================================
#  gui.py
#  Aplicacion: ensamblador de pantallas
# ============================================================

import tkinter as tk
from estilos import COLOR_FONDO
from estados import AlgoritmoBalanceo
from sistema_de_matricula import SistemaDeMatricula
from pantalla_bienvenida import PantallaBienvenida
from pantalla_config import PantallaConfiguracion
from pantalla_juego import PantallaJuego
from pantalla_resultados import PantallaResultados


class Aplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Matrículas Universitarias")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLOR_FONDO)
        self.sistema = None
        self._pantalla_actual = None

    def iniciar(self):
        self._mostrar_bienvenida()
        self.root.mainloop()

    def _limpiar(self):
        if self._pantalla_actual:
            self._pantalla_actual.destroy()

    def _mostrar_bienvenida(self):
        self._limpiar()
        self._pantalla_actual = PantallaBienvenida(self.root, self._rutear_modo)
        self._pantalla_actual.pack(fill="both", expand=True)

    def _rutear_modo(self, es_mision: bool):
        self._limpiar()
        if es_mision:
            self.sistema = SistemaDeMatricula(2, 100, AlgoritmoBalanceo.MENOR_CARGA, modo_misiones=True)
            self._pantalla_actual = PantallaJuego(self.root, self.sistema, self._mostrar_resultados)
            self._pantalla_actual.pack(fill="both", expand=True)
        else:
            self._pantalla_actual = PantallaConfiguracion(self.root, self._iniciar_libre)
            self._pantalla_actual.pack(fill="both", expand=True)

    def _iniciar_libre(self, num_servidores: int, capacidad: int, algoritmo: AlgoritmoBalanceo):
        self.sistema = SistemaDeMatricula(num_servidores, capacidad, algoritmo, modo_misiones=False)
        self._limpiar()
        self._pantalla_actual = PantallaJuego(self.root, self.sistema, self._mostrar_resultados)
        self._pantalla_actual.pack(fill="both", expand=True)

    def _mostrar_resultados(self):
        self._limpiar()
        self._pantalla_actual = PantallaResultados(self.root, self.sistema, self.root.quit)
        self._pantalla_actual.pack(fill="both", expand=True)