import time
from pynput import mouse, keyboard as pynputKey
import keyboard
from eventos import *
import sys
from PyQt6 import uic #importar lo necesario para las interfaces graficas
from PyQt6.QtWidgets import * # importar todos los widgets de la interfaz grafica
from PyQt6 import QtCore
from PyQt6.QtCore import QSize

eventosDict: list[dict] = []
keysList: list[str] = []
initialTime: float
tiempoPrevio: float
mListener: mouse.Listener
kListener: pynputKey.Listener
grabarJson: bool = False
mouseIsMoving: bool = False
mouseIsDown: bool = False
keyIsPressed: bool = False


def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)
		writeJson("secuencia", eventosDict, 2)


def getLastEvent() -> dict:
	last: dict
	try:
		last = eventosDict[-1]	#& Obtener el ultimo evento, pa revisar si es un movimiento reemplazarlo (ir directo al lugar)
	except (IndexError):
		last = {}	#& Json Vacio
	return last


def getEventTime(isEvent: bool = True) -> float:
	"""
	- Retorna por default la diferencia de tiempo desde el ultimo evento
	- Si se le pasa `False` entonces retorna el tiempo desde el ultimo evento, mas no modifica ese tiempo (no cuenta como "evento")
	"""
	global initialTime
	global tiempoPrevio

	tiempoActual: float = time.time() - initialTime
	diff : float = tiempoActual - tiempoPrevio	#& diferencia de tiempos
	# print(f"actual: {tiempoActual:.6f} previo: {tiempoPrevio:.6f} diferencia {diff:.6f}")
	if isEvent:
		tiempoPrevio = tiempoActual

	return float(format(diff, ".6f"))


def mouseClick(x: int, y: int, button: mouse.Button, pressed: bool):
	last = getLastEvent()
	mousePressTime: float
	mouseReleaseTime: float
	if pressed:
		mousePressTime = getEventTime(False)
	else:
		mouseReleaseTime = getEventTime(False)

	mouseDownDuration: float = mouseReleaseTime - mousePressTime
	print("Duration:", mouseDownDuration)
	if(mouseDownDuration <= 0.15):	#& Decimos que se hizo un click y no un hold
		lastTime: float
		if last == {}:
			lastTime = 0
		else:
			lastTime = last.get("timeSince")

		diff : float = getEventTime()
		resta: float = float(format(diff - lastTime, ".6f"))	#& Resta en Segundos, segun windows el tiempo mayor pa un doble click son 500ms
		if(last.get("name") == "click_left" and button == mouse.Button.left and resta <= 0.5):
			if(last.get("x") == x and last.get("y") == y):	#& Si es un click en la misma posocion en menos de medio segundo
				last["timeSince"] = float(format((diff + lastTime), ".6f"))
				last["times"] = last["times"] + 1
				# print(f"PastLeftClick times:{last["times"]} | Diff:{diff:.6f} - LastTime:{lastTime:.6f} = Resta:{resta:.6f}")
				return

		if button == mouse.Button.left:
			print("LeftClick")
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : diff,
				"times" : 1,	#& times es solo necesario y posible en el click izquierdo
				"x" : x,
				"y" : y
			})
		else:
			print("SomeClick")
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : diff,
				"x" : x,
				"y" : y
			})
	else:	#& Decimos que es un hold
		diff : float = getEventTime()
		hold = {
			"name" : "mouseDown",
			"timeSince" : diff,
			"button" : f"{button.name}"
		}
		release = {
			"name" : "mouseUp",
			"timeSince" : mouseDownDuration,
			"button" : f"{button.name}"
		}
		if(last.get("name") == "mouseMove"):	#& Si se hizo un movimiento antes del hold, o mejor dicho, probablemente durante
			eventosDict.insert(-1, hold)	#& inserto el Hold antes del movimiento
			eventosDict.append(release)		#& Añado el Release despues del movimiento
		else:
			eventosDict.append(hold)
			eventosDict.append(release)


def mouseMove(x: int, y:int):
	diff: float = getEventTime(False)
	last = getLastEvent()
	if(last.get("name") == "mouseMove"):
		lastTime: float = last.get("timeSince")
		last["timeSince"] = float(format(lastTime+diff, ".6f"))	#& Tiempo anterior + el actual
		last["x"] = x
		last["y"] = y
		return
	else:
		diff = getEventTime()
		eventosDict.append({
			"name" : "mouseMove",
			"timeSince" : diff,
			"x" : x,
			"y" : y
		})


def mouseScroll(x: int, y:int, dx: int, dy: int):
	"""
	x = pos del mouse en X
	y = pos del mouse en Y
	dx = Scroll Horitzontal al parecer
	dy = Hacia donde se hizo scroll (Menor a 0 es pa arriba, mayor pa abajo)
	"""
	# print(f"x:{x} | y:{y} | dx:{dx} | dy{dy}")
	diff: float = getEventTime()
	eventosDict.append({
		"name" : "mouseScroll",
		"timeSince" : diff,
		"dx" : dx,
		"dy" : dy
	})


def keyPress(key: pynputKey.Key):
	print(key.name)


def keyRelease(key: pynputKey.Key):
	if key == pynputKey.Key.esc:
		global mListener, kListener, window
		mListener.stop()	#& MouseListener Detenido
		kListener.stop()	#& KeyListener Detenido
		# writeJson("secuencia", eventosDict, 2)	#& Modificar Json
		# print("Nuevo Json Guardado")
		# window.showNormal()
		# window.show()
		# window.update()
		callEventos(eventosDict)


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

	with mouse.Listener(on_click=mouseClick, on_move=mouseMove, on_scroll=mouseScroll) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
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
		self.widget = QWidget()#este elemento contrendra el layout
		self.layout = QVBoxLayout()#en este layout podremos agregar elementos nuevos
		self.layout.setContentsMargins(15, 20, 20, 20)#le pongo margenes a donde se ponen los labels que agregarre , porque sino quedan todos pegados a la izquierda
		self.widget.setLayout(self.layout)
		self.AreaDeBloques = self.scrollArea1#esta scroll area es para hacer el efecto ese de bajar entre los bloques
		self.AreaDeBloques.setWidgetResizable(True)
		self.AreaDeBloques.setWidget(self.widget)


		for i in range(1, 50):
			label = QLabel(f"Label {i}")
			# label.setStyleSheet(u"QLabel{text-align: center;}")
			self.layout.addWidget(label)
			label.setFixedSize(QSize(220,60))
			
		#global grabarJson
		#if(grabarJson):
		#	grabar()
		#else:
		#	ejecutar()


if __name__ == "__main__": #&name es una variable de python , contiene el nombre del script
							#& osea aqui preguntamos , si este script es el modulo principal
							#+ Asi es, y por eso metere la funcion "main" aqui
	# main()
	grabar()	#& Probando directamente los listener, sin nececidad de la GUI