import time
from pynput import mouse, keyboard as pynputKey
import keyboard
from eventos import *
import sys
from PyQt6 import uic #importar lo necesario para las interfaces graficas
from PyQt6.QtWidgets import * # importar todos los widgets de la interfaz grafica
from PyQt6.QtWidgets import QKeySequenceEdit
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize, pyqtSignal
from datetime import datetime
from PyQt6.QtGui import QIntValidator
import threading

eventosDict: list[dict] = []
keysList: list[str] = []
initialTime: float
tiempoPrevio: float
mListener: mouse.Listener | None = None
kListener: pynputKey.Listener | None = None
grabarJson: bool = False
mouseIsMoving: bool = False
mouseIsDown: bool = False
keyIsPressed: bool = False
NombreNuevaSecuencia : str 
TiempoDeRepeticion = 0

""" 
def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)
		writeJson("secuencia", eventosDict, 2)
"""

def getLastEvent(x:int = -100, y:int = -100) -> dict:
	global eventosDict
	last: dict
	try:
		last = eventosDict[-1]	#& Obtener el ultimo evento, pa revisar si es un movimiento reemplazarlo (ir directo al lugar)
	except (IndexError):
		if(x != -100 and y != -100):
			last = {
				"name" : "mouseMove",
				"timeSince" : 0,
				"x" : x,
				"y" : y
			}
			eventosDict.append(last)
		else:
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

""" 
def mouseClick(x: int, y: int, button: mouse.Button, pressed: bool):
	last = getLastEvent()
	mousePressTime: float = 0.0
	mouseReleaseTime: float = 0.0
	if pressed:
		mousePressTime = getEventTime(False)
	if not pressed:
		mouseReleaseTime = getEventTime(False)
	diff : float = getEventTime()

	mouseDownDuration: float = diff - (mouseReleaseTime + mousePressTime)
	print(f"DownDuration:{mouseDownDuration} = Release:{mouseReleaseTime} + Press:{mousePressTime} - diff:{diff}")	
	if(mouseDownDuration <= 0.15):	#& Decimos que se hizo un click y no un hold
		lastTime: float
		if last == {}:
			eventosDict.append({
				"name" : "startPos",
				"timeSince" : diff,
				"x" : x,
				"y" : y,
			})
			lastTime = 0
		else:
			lastTime = last.get("timeSince")

		
		resta: float = float(format(diff - lastTime, ".6f"))	#& Resta en Segundos, segun windows el tiempo mayor pa un doble click son 500ms
		if(last.get("name") == "click_left" and button == mouse.Button.left and resta <= 0.5):
			if(last.get("x") == x and last.get("y") == y):	#& Si es un click en la misma posocion en menos de medio segundo
				last["timeSince"] = float(format((diff + lastTime), ".6f"))
				last["times"] = last["times"] + 1
				print(f"PastLeftClick times:{last["times"]} | Diff:{diff:.6f} - LastTime:{lastTime:.6f} = Resta:{resta:.6f}")
				return

		elif button == mouse.Button.left:
			print("LeftClick")
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : diff,
				"times" : 1,	#& times es solo necesario y posible en el click izquierdo
				"x" : x,
				"y" : y
			})
		else:
			# print("SomeClick")
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
"""

def mouseClick(x: int, y: int, button: mouse.Button, pressed: bool):
	global eventosDict
	getLastEvent(x, y)
	diff : float = getEventTime()
	event: dict
	if pressed:	#& Decimos que es un hold
		event = {
			"name" : "mouseDown",
			"timeSince" : diff,
			"button" : f"{button.name}"
		}
	else:
		event = {
			"name" : "mouseUp",
			"timeSince" : diff,
			"button" : f"{button.name}"
		}
	
	eventosDict.append(event)
	if not pressed: #& Si se solto el mouse
		checkMouseClick(x, y, button)


def checkMouseClick(x:int, y:int, button: mouse.Button):
	"""
	Solo se llama una vez se solto el mouse, por lo tanto siempre deberia existir un evento antes de esto
	"""
	global eventosDict
	mouseDownEvent: dict = eventosDict[-2]	#& Si los 2 ultimos, este es cuando se presiona
	mouseUpEvent: dict = eventosDict[-1]	#& Si los 2 ultimos, este es cuando se libera
	# print("\tDown:",mouseDownEvent)
	# print("\tUp:",mouseUpEvent)

	if (mouseUpEvent.get("name") != "mouseUp" and mouseDownEvent.get("name") != "mouseDown"):
		return

	#& Si llega aqui, es porque los 2 de arriba NO se cumplen, osea ambos son iguales
	downTime: float = mouseDownEvent["timeSince"]
	upTime: float = mouseUpEvent["timeSince"]
	diff: float = abs(downTime - upTime)	#& Ver la diferencia de tiempo entre esos 2 eventos (abs porque aveces daba - , ya vale vrga, sigue siendo su diferencia)
									#& se resta el down - up, porque el Up es el que muestra la diferencia real de tiempo entre ambos
									#& Si el up es el que es los 150ms despues, entonces es que fue un hold, si no, un click

	if(diff <= 0.15): #& Si la diferencia entre ambos click es menos de 150ms
		# print(f"Count as Click | diff:{diff} = upTime:{upTime} - downTime:{downTime}")
		eventosDict.pop()
		eventosDict.pop()
		eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : float(format(upTime+downTime, ".6f")),
				"x" : x,
				"y" : y
			})


def mouseMove(x: int, y:int):
	global eventosDict
	diff: float = getEventTime()
	last = getLastEvent()
	if(last.get("name") == "mouseMove"):
		lastTime: float = last.get("timeSince")
		last["timeSince"] = float(format(lastTime+diff, ".6f"))	#& Tiempo anterior + el actual
		last["x"] = x
		last["y"] = y
		return
	else:
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
	global eventosDict
	getLastEvent(x, y)
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
		global mListener, kListener, window, grabarJson, NombreNuevaSecuencia
		mListener.stop()	#& MouseListener Detenido
		kListener.stop()	#& KeyListener Detenido
		mListener = None
		kListener = None
		writeJson(NombreNuevaSecuencia, lista=eventosDict, indentacion=2)	#& Modificar Json
		print("Nuevo Json Guardado")
		grabarJson = False
		window.end_grabar.emit()
		window.normalizarVentana.emit()
		# window.showNormal()
		# window.show()
		# window.update()
		# print("Start")
		# callEventos(eventosDict)	#& TODO: Se tiene que eliminar de aqui despues al tener el boton pa ejecutar
		# print("End")


def main():
	global window
	app = QApplication(sys.argv)
	window = Pantalla()
	sys.exit(app.exec())
	""" 
	#& Todo ese codigo anterior en comentarios pa evitar eliminar cosas utiles, de momento
	global initialTime	#& Para cambiar directamente los valores de las variables globales (Si no solo seria dentro de esta funcion)
	global tiempoPrevio
	global grabarJson

	desicion = input("Desea Grabar el Json? (y/n) : si no lo graba se ejecutara el ya guardado\n") #& Pa diferenciar despues cuando andamos guardando o ejecutando la secuencia del Json
	if desicion.lower() == "y":
		grabarJson = True
	else:
		grabarJson = False


	initialTime = time.time()
	tiempoPrevio = 0.0
	if grabarJson:
		with mouse.Listener(on_click=mouseClick) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
			mouseListener.join()
			keyListener.join()
		

		keyboard.on_press(eventoTeclado)
		keyboard.wait("esc")

	else:
		dicc = readJson("secuence")	#& Tambien imprime el json leido, de momento almenos
		callEventos(dicc)
	"""


def grabar():
	
	global eventosDict
	eventosDict.clear()
	global initialTime	#& Para cambiar directamente los valores de las variables globales (Si no solo seria dentro de esta funcion)
	global tiempoPrevio
	global grabarJson
	global mListener, kListener
	# global window

	window.minimizarVentana.emit()

	initialTime = time.time()
	tiempoPrevio = 0.0

	mListener = pynput.mouse.Listener(on_click=mouseClick, on_move=mouseMove, on_scroll=mouseScroll)
	kListener = pynputKey.Listener(on_press=keyPress, on_release=keyRelease)
	print("Pulsa \"escape\" para terminar la grabacion (Aun No graba Teclas, no lo eh combinado - Jaiber)")
	mListener.start()
	kListener.start()

	"""
	with mouse.Listener(on_click=mouseClick, on_move=mouseMove, on_scroll=mouseScroll) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
			global mListener, kListener
			mListener = mouseListener	#& Asignarlos a las variables globales
			kListener = keyListener
			print("Pulsa \"escape\" para terminar la grabacion (Aun No graba Teclas, no lo eh combinado - Jaiber)")
			mListener.join()
			kListener.join()
	"""


def ejecutar(name: str = "testSecuencia"):
	diccionarioJson: dict = readJson(name)
	callEventos(diccionarioJson)


class Pantalla(QDialog):
	end_grabar = pyqtSignal()	#& Signal para que cuando el hilo de grabar se detenga, se llame a generar los bloques
	minimizarVentana = pyqtSignal()
	normalizarVentana = pyqtSignal()
	def __init__(self):
		super(Pantalla, self).__init__()
		uic.loadUi("interfaz.ui", self)
		self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowMaximizeButtonHint) #& Minimizar/Maximizar
		self.setWindowTitle("mas nunca en mi vida usare python")
		self.frames = []
		self.botonGrabar: QToolButton = self.GRABAR
		self.botonEjecutar: QToolButton = self.EJECUTAR
		self.botonIniciar: QToolButton = self.INICIAR 
		self.labelApartado: QLabel = self.TextoDelApartado
		self.TiempoIngresado = self.lineEdit_2

		intValidator = QIntValidator()
		self.TiempoIngresado.setValidator(intValidator)


		self.radioButtonSegundos = self.radioButton
		self.radioButtonHora = self.radioButton_2
		self.radioButtonMinutos = self.radioButton_3

		self.radioButtonSegundos.toggled.connect(self.establecerTiempoDeRepeticion)
		self.radioButtonHora.toggled.connect(self.establecerTiempoDeRepeticion)
		self.radioButtonMinutos.toggled.connect(self.establecerTiempoDeRepeticion)

		

		#apartado de la derecha 
		self.widgetDerecha = QWidget()#este elemento contrendra el layout
		self.layoutDerecha = QVBoxLayout()#en este layout podremos agregar elementos nuevos
		self.layoutDerecha.setContentsMargins(15, 20, 20, 20)#le pongo margenes a donde se ponen los labels que agregarre , porque sino quedan todos pegados a la izquierda
		self.widgetDerecha.setLayout(self.layoutDerecha)
		self.AreaDeBloques2 = self.scrollArea2#esta scroll area es para hacer el efecto ese de bajar entre los bloques
		self.AreaDeBloques2.setWidgetResizable(True)
		self.AreaDeBloques2.setWidget(self.widgetDerecha)

		#apartado de la izquierda
		self.widgetIzquierda = QWidget()#este elemento contrendra el layout
		self.layoutIzquierda = QVBoxLayout()#en este layout podremos agregar elementos nuevos
		self.layoutIzquierda.setContentsMargins(15, 20, 20, 20)#le pongo margenes a donde se ponen los labels que agregarre , porque sino quedan todos pegados a la izquierda
		self.widgetIzquierda.setLayout(self.layoutIzquierda)
		self.AreaDeBloques = self.scrollArea1#esta scroll area es para hacer el efecto ese de bajar entre los bloques
		self.AreaDeBloques.setWidgetResizable(True)
		self.AreaDeBloques.setWidget(self.widgetIzquierda)

		self.show()
		self.IniciarBloques()

		self.botonGrabar.clicked.connect(self.TextoGrabar)
		self.botonEjecutar.clicked.connect(self.TextoEjecutar)
		self.botonIniciar.clicked.connect(self.BotonIniciar)

	def eliminarBloquesDerecha(self):
		for i in range (self.layoutDerecha.count()):
			bloque = self.layoutDerecha.itemAt(i).widget()
			bloque.deleteLater()

	def TextoGrabar(self) :
		self.labelApartado.setText("Grabe o seleccione una secuencia para ser mostrada.")
		global grabarJson
		grabarJson = True	#& Se grabara el Json cuando se pulde el boton de iniciar
		self.botonIniciar.setText("Grabar >")
		self.eliminarBloquesDerecha()
		print("Preparado para Grabar Json ...")

	def TextoEjecutar(self) :
		self.labelApartado.setText("Secuencia:")    
		global grabarJson
		grabarJson = False	#& Se ejecutara/Creara (idk) cuando se pulse el boton de iniciar
		self.botonIniciar.setText("Ejecutar >")
		print("Preparado para Ejecutar Json ...")



	def establecerTiempoDeRepeticion(self, checked):
		global TiempoDeRepeticion
		if checked:
			if self.sender() is self.radioButtonSegundos:
				TiempoDeRepeticion = int(self.TiempoIngresado.text())
				# Realizar acciones para la opción 1
			elif self.sender() is self.radioButtonMinutos:
				TiempoDeRepeticion = int(self.TiempoIngresado.text()) * 60
				# Realizar acciones para la opción 2
			elif self.sender() is self.radioButtonHora :
				TiempoDeRepeticion = int(self.TiempoIngresado.text()) * 3600
				# Realizar acciones para la opción 2


	def AgregarNuevoBloque(self):
		global grabarJson, NombreNuevaSecuencia

		self.IngresoDeNombre:QLineEdit = self.lineEdit
		NombreNuevaSecuencia = self.IngresoDeNombre.text() ###########################luego reviso esto para cambiarlo
		self.NombreNuevoBloque = self.IngresoDeNombre.text()
		self.nuevoBoton = QToolButton()
		self.nuevoBoton.setStyleSheet("""
	QToolButton {
		background: #FF4A1C;
		color: #fff;
		padding: 10px 20px;
		border: none;
		border-radius: 3px;
		min-width: 148px;
		min-height: 10px;
		max-width: 148px;
		max-height: 10px;
	}
	QToolButton:hover {
		background-color: blue;
		color: white;
	}
""")


		if(self.NombreNuevoBloque == ""):
			self.NombreNuevoBloque = str(datetime.now())	

		self.nuevoBoton.setText(self.NombreNuevoBloque)
		self.layoutIzquierda.addWidget(self.nuevoBoton)
		self.nuevoBoton.clicked.connect(self.manejar_click)
		self.IngresoDeNombre.clear()
		grabarJson = False
		self.botonIniciar.setText("Ejecutar >")



	def manejar_click(self):
		global grabarJson
		boton = self.sender()  # Obtiene el botón que envió la señal
		self.nuevoBoton = QToolButton()
		self.nuevoBoton.setStyleSheet("""
		QToolButton {
		background: #F24236;
		color: #fff;
		padding: 10px 20px;
		border: none;
		border-radius: 5px;
		min-width: 420px;
		min-height: 30px;
		max-width: 420px;
		max-height: 30px;
	}
	QToolButton:hover {
		background-color: blue;
		color: white;
	}
""")		
		

		if(grabarJson == False):
			self.nuevoBoton.setText(boton.text())
			self.layoutDerecha.addWidget(self.nuevoBoton)
			print(f"Botón presionado: {self.nuevoBoton.text()}")
			self.botonSecuencia.clicked.connect(self.manejar_click)




	def ejecucion(self):
		global TiempoDeRepeticion
		if(self.layoutDerecha.count() != 0):
			for i in range(self.layoutDerecha.count()):
				print(f"ejecutando la Secuencia {self.layoutDerecha.itemAt(i).widget().text()}")
				ejecutar(self.layoutDerecha.itemAt(i).widget().text())
		
		hiloRepeticiones = threading.Timer(TiempoDeRepeticion, self.ejecucion)
		hiloRepeticiones.start()

	def BotonIniciar(self):
		global grabarJson
		if(grabarJson):
			self.AgregarNuevoBloque()
			grabar()
		else:
			self.ejecucion()


	def IniciarBloques(self):
		secuenciasUsuario: list[str] = getJsons()
		for index, value in enumerate(secuenciasUsuario):
			self.botonSecuencia = QToolButton()
			self.botonSecuencia.setStyleSheet("""
	QToolButton {
		background: #FF4A1C;
		color: #fff;
		padding: 10px 20px;
		border: none;
		border-radius: 3px;
		min-width: 148px;
		min-height: 10px;
		max-width: 148px;
		max-height: 10px;
	}
	QToolButton:hover {
		background-color: blue;
		color: white;
	}
""")
			self.layoutIzquierda.addWidget(self.botonSecuencia)	#! QObject::setParent: Cannot set parent, new parent is in a different thread
			self.botonSecuencia.setFixedSize(QSize(220,60))
			self.botonSecuencia.setText(value.replace(".json",""))
			self.botonSecuencia.clicked.connect(self.manejar_click)

	def keyPressEvent(self, event: QtGui.QKeyEvent):
		if event.key() == QtCore.Qt.Key.Key_Escape: #& Escape Key code in PyQt6
			print("Esc Pressed in Qt")
			event.ignore()
		else:
			event.accept()

	def Minimizar(self):
		print("minimizado")
		self.showMinimized()

	def Normalizar(self):
		print("normalizado")
		self.showNormal()

if __name__ == "__main__": #&name es una variable de python , contiene el nombre del script
							#& osea aqui preguntamos , si este script es el modulo principal
							#+ Asi es, y por eso metere la funcion "main" aqui
	main()
	# grabar()	#& Probando directamente los listener, sin nececidad de la GUI