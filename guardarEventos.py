import time
from pynput import mouse, keyboard as pynputKey
import keyboard
from eventos import *
import sys
from PyQt6 import uic #importar lo necesario para las interfaces graficas
from PyQt6.QtWidgets import * # importar todos los widgets de la interfaz grafica
from PyQt6 import QtCore

initialTime: float
tiempoPrevio: float
mListener: mouse.Listener
kListener: pynputKey.Listener
grabarJson: bool = False
eventosDict: list[dict] = []
keysPressed: list[str] = []


def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)
		writeJson("secuencia", eventosDict, 2)


def mouseClick(x: int, y: int, button: mouse.Button, pressed: bool):
	if pressed:
		global initialTime
		global tiempoPrevio

		tiempoActual: float = time.time() - initialTime
		diff : float = tiempoActual - tiempoPrevio	#& diferencia de tiempos
		print(f"actual: {tiempoActual:.6f} previo: {tiempoPrevio:.6f} diferencia {diff:.6f}")
		tiempoPrevio = tiempoActual


		if button == mouse.Button.middle:
			print("Botón medio presionado. Deteniendo el listener.")
			return False

		if button == mouse.Button.left or button == mouse.Button.right:
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : float(format(diff, ".3f")),
				"x": x,
				"y" : y
			})


def keyPress(key: pynputKey.Key):
	print(key.name)


def keyRelease(key: pynputKey.Key):
	if key == pynputKey.Key.esc:
		global mListener, kListener, window
		mListener.stop()	#& MouseListener Detenido
		kListener.stop()	#& KeyListener Detenido
		writeJson("secuencia", eventosDict, 2)	#& Modificar Json
		print("Nuevo Json Guardado")
		# window.showNormal()
		# window.show()
		# window.update()

def main():
	global window
	app = QApplication(sys.argv)
	window = Pantalla()
	sys.exit(app.exec())

	#& Todo ese codigo anterior en comentarios pa evitar eliminar cosas utiles, de momento
	# global initialTime	#& Para cambiar directamente los valores de las variables globales (Si no solo seria dentro de esta funcion)
	# global tiempoPrevio
	# global grabarJson

	# desicion = input("Desea Grabar el Json? (y/n) : si no lo graba se ejecutara el ya guardado\n") #& Pa diferenciar despues cuando andamos guardando o ejecutando la secuencia del Json
	# if desicion.lower() == "y":
	# 	grabarJson = True
	# else:
	# 	grabarJson = False


	# initialTime = time.time()
	# tiempoPrevio = 0.0
	# if grabarJson:
	# 	with mouse.Listener(on_click=mouseClick) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
	# 		mouseListener.join()
	# 		keyListener.join()
		

	# 	keyboard.on_press(eventoTeclado)
	# 	keyboard.wait("esc")

	# else:
	# 	dicc = readJson("secuence")	#& Tambien imprime el json leido, de momento almenos
	# 	callEventos(dicc)

def grabar():
	global initialTime	#& Para cambiar directamente los valores de las variables globales (Si no solo seria dentro de esta funcion)
	global tiempoPrevio
	global grabarJson
	global window

	# window.showMinimized()

	initialTime = time.time()
	tiempoPrevio = 0.0

	with mouse.Listener(on_click=mouseClick) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
			global mListener, kListener
			mListener = mouseListener	#& Asignarlos a las variables globales
			kListener = keyListener
			print("Pulsa \"escape\" para terminar la grabacion (Aun No graba Teclas, no lo eh combinado - Jaiber)")
			mListener.join()
			kListener.join()

def ejecutar():
	diccionarioJson: dict = readJson("secuencia")
	callEventos(diccionarioJson)

class Pantalla(QDialog):

	def __init__(self):
		super(Pantalla, self).__init__()
		uic.loadUi("interfaz.ui", self)
		self.setWindowTitle("mas nunca en mi vida usare python")
		self.frames = []
		self.botonGrabar: QToolButton = self.GRABAR
		self.botonEjecutar: QToolButton = self.EJECUTAR
		self.botonIniciar: QToolButton = self.INICIAR 
		self.labelApartado: QLabel = self.TextoDelApartado

		self.show()

		self.botonGrabar.clicked.connect(self.TextoGrabar)
		self.botonEjecutar.clicked.connect(self.TextoEjecutar)
		self.botonIniciar.clicked.connect(self.IniciarBoton)

	def TextoGrabar(self) :
		self.labelApartado.setText("Grabe o seleccione una secuencia para ser mostrada.")
		global grabarJson
		grabarJson = True	#& Se grabara el Json cuando se pulde el boton de iniciar
		self.botonIniciar.setText("Grabar >")
		print("Preparado para Grabar Json ...")

	def TextoEjecutar(self) :
		self.labelApartado.setText("Secuencia:")    
		global grabarJson
		grabarJson = False	#& Se ejecutara/Creara (idk) cuando se pulse el boton de iniciar
		self.botonIniciar.setText("Ejecutar >")
		print("Preparado para Ejecutar Json ...")

	def IniciarBoton(self):
		global grabarJson
		if(grabarJson):
			grabar()
		else:
			ejecutar()


if __name__ == "__main__": #&name es una variable de python , contiene el nombre del script
							#& osea aqui preguntamos , si este script es el modulo principal
							#+ Asi es, y por eso metere la funcion "main" aqui
	main()