import time
from pynput import mouse, keyboard as pynputKey
import keyboard
from eventos import *
import sys
from PyQt6 import uic #importar lo necesario para las interfaces graficas
from PyQt6.QtWidgets import * # importar todos los widgets de la interfaz grafica

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
		mouseListener.stop()
		return False



print("Iniciado")
desicion = input("Desea Grabar el Json? (y/n) : si no lo graba se ejecutara el ya guardado") #& Pa diferenciar despues cuando andamos guardando o ejecutando la secuencia del Json
if desicion.lower() == "y":
	grabarJson = True
else:
	grabarJson = False


initialTime: float = time.time()
tiempoPrevio: float = 0.0
if grabarJson:
	with mouse.Listener(on_click=mouseClick) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
		mouseListener.join()
		keyListener.join()
	

	keyboard.on_press(eventoTeclado)
	keyboard.wait("esc")

else:
	dicc = readJson("secuence")	#& Tambien imprime el json leido, de momento almenos
	callEventos(dicc)





class pantalla(QDialog):
	def __init__(self):
		super(pantalla, self).__init__()
		uic.loadUi("interfaz.ui", self)
		self.setWindowTitle("mas nunca en mi vida usare python")
		self.frames = []

		self.show()

		self.GRABAR.clicked.connect(self.TextoGrabar)
		self.EJECUTAR.clicked.connect(self.TextoEjecutar)

	def TextoGrabar(self) :
		self.TextoDelApartado.setText("Grabe o seleccione una secuencia para ser mostrada.")

	def TextoEjecutar(self) :
		self.TextoDelApartado.setText("Secuencia:")    

if __name__ == "__main__": #name es una variable de python , contiene el nombre del script
                            # osea aqui preguntamos , si este script es el modulo principal
    app = QApplication(sys.argv)
    dia = pantalla()
    sys.exit(app.exec())      	