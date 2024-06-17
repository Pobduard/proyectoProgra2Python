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


"""
&	Autores:
&	Jesus Miguel Mora Colmenares	C.I: 30.351.836
&	Jaiber Eduardo Arellano Ibarra	C.I: 30.338.584
"""

pyautogui.FAILSAFE = False	#& Desactivar el FailSafe que posee PyAutoGui, ya tenemos las cosas que se puedan detener sin problemas
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
TiempoDeRepeticion: int = 1
secuenciasCargadas: bool = False
EnModoEliminaar: bool = False
hiloProcesoEjecucion: threading.Thread
hiloProcesoGrabar: threading.Thread
enEjecucion: bool = False
enGrabado: bool = False
currentPressGrabar: set[pynputKey.Key] = set()


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


def keyPressGrabar(key: pynputKey.Key):
	global currentPressGrabar
	print(key, "Actuales:", len(currentPressGrabar))
	if key == pynputKey.Key.esc:
		global mListener, kListener, window, grabarJson, NombreNuevaSecuencia, enGrabado
		mListener.stop()	#& MouseListener Detenido
		kListener.stop()	#& KeyListener Detenido
		mListener = None
		kListener = None
		writeJson(NombreNuevaSecuencia, lista=eventosDict, indentacion=2)	#& Modificar Json
		print("Nuevo Json Guardado")
		enGrabado = False
	if(key == pynputKey.Key.ctrl or key == pynputKey.Key.ctrl_l or key == pynputKey.Key.ctrl_r):
#& TODO: CONTROL
		print(key)	
		return
	else:
		currentPressGrabar.add(key)
		return

def keyReleaseGrabar(key: pynputKey.Key):
	global currentPressGrabar
	long: int = len(currentPressGrabar)

	if(long == 1):
		tecla = key.char if (type(key) == pynput.keyboard.KeyCode) else (key.name)
		print("Released: ", tecla)
#& TODO: Añadir Accion
	else:	#+ < 1
		teclas = [t.name if type(t) == pynput.keyboard.Key else t.char for t in currentPressGrabar]
		print("Multiple Released: ", teclas)
#& TODO: Añadir Accion

	currentPressGrabar.clear()	#& Cada vez que se deja de pulsar, se limpia TODAS las letras actuales (Si es una combinacion, se pulsarian a la vez de todas formas)

def keyPressEjecutar(key: pynputKey.Key):
	if key == pynputKey.Key.esc:
		global kListener, window
		window.stopKeyListenerSignal.emit()

def keyReleaseEjecutar(key: pynputKey.KeyCode):
	print(f"Released: {key.char}")


def main():
	global window
	app = QApplication(sys.argv)
	window = Pantalla()
	sys.exit(app.exec())


def grabar():
	global eventosDict
	eventosDict.clear()
	global initialTime	#& Para cambiar directamente los valores de las variables globales (Si no solo seria dentro de esta funcion)
	global tiempoPrevio
	global enGrabado
	global mListener, kListener
	global window

	initialTime = time.time()
	tiempoPrevio = 0.0

	mListener = pynput.mouse.Listener(on_click=mouseClick, on_move=mouseMove, on_scroll=mouseScroll)
	kListener = pynputKey.Listener(on_press=keyPressGrabar, on_release=keyReleaseGrabar)
	print("Pulsa \"escape\" para terminar la grabacion (Aun No graba Teclas, no lo eh combinado - Jaiber)")
	mListener.start()
	kListener.start()

	while enGrabado:
		time.sleep(1)	#& Para que ojala el hilo se mantenga activo
	print("EndGrabar")
	window.normalizarVentana.emit()	#& Final de hilo


def ejecutar(name: str = "testSecuencia"):
	diccionarioJson: dict = readJson(name)
	callEventos(diccionarioJson)


class Pantalla(QDialog):
	end_grabar = pyqtSignal()	#& Signal para que cuando el hilo de grabar se detenga, se llame a generar los bloques
	minimizarVentana = pyqtSignal()
	normalizarVentana = pyqtSignal()
	stopKeyListenerSignal = pyqtSignal()

	def __init__(self):
		super(Pantalla, self).__init__()
		uic.loadUi("interfaz.ui", self)
		self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowMaximizeButtonHint) #& Minimizar/Maximizar
		self.setWindowTitle("PyDesk")
		self.frames: list = []
		self.botonGrabar: QToolButton = self.GRABAR
		self.botonEjecutar: QToolButton = self.EJECUTAR
		self.botonIniciar: QToolButton = self.INICIAR 
		self.labelApartado: QLabel = self.TextoDelApartado
		self.TiempoIngresado: QLineEdit = self.lineEdit_2
		self.ApartadoIngresarNombre: QLineEdit = self.NombreDelBloque
		self.ApartadoIngresarTiempoDeRepeticion: QLineEdit = self.NombreDelBloque_2
		self.ApartadoTextpGrabar: QLabel = self.FrameDelApartadoGrabar
		self.ApartadoTextpEjecutar: QLabel = self.FrameDelApartadoEjecutar
		self.ApartadoTextElegirModo: QLabel = self.FrameDelApartadoElegirModo
		self.ApartadoTextModoEliminar: QLabel = self.FrameDelApartadoModoEliminar
		self.BotonModoEliminar: QToolButton = self.BotonModoEliminar

		self.ApartadoTextpEjecutar.setVisible(False)
		self.ApartadoTextpGrabar.setVisible(False)
		self.ApartadoTextModoEliminar.setVisible(False)


		self.BotonModoEliminar.setVisible(False)
		self.botonIniciar.setVisible(False)
		self.ApartadoIngresarNombre.setVisible(False)
		self.ApartadoIngresarTiempoDeRepeticion.setVisible(False)

		intValidator = QIntValidator()
		self.TiempoIngresado.setValidator(intValidator)
		self.TiempoIngresado.setText("")


		self.radioButtonSegundos: QRadioButton = self.radioButton
		self.radioButtonHora: QRadioButton = self.radioButton_2
		self.radioButtonMinutos: QRadioButton = self.radioButton_3

		self.radioButtonSegundos.setChecked(True)
		self.radioButtonSegundos.toggled.connect(self.establecerTiempoDeRepeticion)
		self.radioButtonHora.toggled.connect(self.establecerTiempoDeRepeticion)
		self.radioButtonMinutos.toggled.connect(self.establecerTiempoDeRepeticion)


		#apartado de la derecha 
		self.widgetDerecha = QWidget()#este elemento contrendra el layout
		self.layoutDerecha = QVBoxLayout()#en este layout podremos agregar elementos nuevos
		self.layoutDerecha.setContentsMargins(15, 20, 20, 20)#le pongo margenes a donde se ponen los labels que agregarre , porque sino quedan todos pegados a la izquierda
		self.widgetDerecha.setLayout(self.layoutDerecha)
		self.AreaDeBloques2: QScrollArea = self.scrollArea2#esta scroll area es para hacer el efecto ese de bajar entre los bloques
		self.AreaDeBloques2.setWidgetResizable(True)
		self.AreaDeBloques2.setWidget(self.widgetDerecha)

		#apartado de la izquierda
		self.widgetIzquierda = QWidget()#este elemento contrendra el layout
		self.layoutIzquierda = QVBoxLayout()#en este layout podremos agregar elementos nuevos
		self.layoutIzquierda.setContentsMargins(15, 20, 20, 20)#le pongo margenes a donde se ponen los labels que agregarre , porque sino quedan todos pegados a la izquierda
		self.widgetIzquierda.setLayout(self.layoutIzquierda)
		self.AreaDeBloques: QScrollArea = self.scrollArea1#esta scroll area es para hacer el efecto ese de bajar entre los bloques
		self.AreaDeBloques.setWidgetResizable(True)
		self.AreaDeBloques.setWidget(self.widgetIzquierda)

		self.show()
		
		self.BotonModoEliminar.clicked.connect(self.ModoEliminar)
		self.botonGrabar.clicked.connect(self.TextoGrabar)
		self.botonEjecutar.clicked.connect(self.TextoEjecutar)
		self.botonIniciar.clicked.connect(self.BotonIniciar)
		self.minimizarVentana.connect(self.Minimizar)
		self.normalizarVentana.connect(self.Normalizar)
		self.stopKeyListenerSignal.connect(self.stopHiloEjecucion)


	def eliminarBloquesDerecha(self):
		for i in range (self.layoutDerecha.count()):
			bloque = self.layoutDerecha.itemAt(i).widget()
			bloque.deleteLater()

	def eliminarBloquesIzquierda(self):
		for i in range(self.layoutIzquierda.count()):
			bloque = self.layoutIzquierda.itemAt(i).widget()
			bloque.deleteLater()

	def eliminarBloqueIndividual(self):
		boton = self.sender()
		print(f"Deleted {boton.text()}")
		deleteFile(boton.text())
		boton.deleteLater()


	def ModoEliminar(self):
		global EnModoEliminaar
		self.eliminarBloquesDerecha()

		if(EnModoEliminaar == False):
			self.ApartadoTextpEjecutar.setVisible(False)
			self.ApartadoTextElegirModo.setVisible(False)
			self.ApartadoTextModoEliminar.setVisible(True)
			self.ApartadoTextpGrabar.setVisible(False)

			for i in range (self.layoutDerecha.count()):
				if(self.layoutDerecha.count() > 0):
					bloque = self.layoutDerecha.itemAt(i).widget()
					bloque.clicked.connect(self.eliminarBloqueIndividual)

			for i in range (self.layoutIzquierda.count()):
				bloque = self.layoutIzquierda.itemAt(i).widget()
				bloque.disconnect()
				bloque.clicked.connect(self.eliminarBloqueIndividual)

			EnModoEliminaar = True	
		
		else:

			self.ApartadoTextpEjecutar.setVisible(True)
			self.ApartadoTextElegirModo.setVisible(False)
			self.ApartadoTextModoEliminar.setVisible(False)
			self.ApartadoTextpGrabar.setVisible(False)

			for i in range (self.layoutDerecha.count()):
				if(self.layoutDerecha.count() > 0):
					bloque = self.layoutDerecha.itemAt(i).widget()
					bloque.disconnect()
					

			for i in range (self.layoutIzquierda.count()):
				bloque = self.layoutIzquierda.itemAt(i).widget()
				bloque.disconnect()
				bloque.clicked.connect(self.manejar_click)

			EnModoEliminaar = False


	def TextoGrabar(self) :
		global secuenciasCargadas
		self.botonIniciar.setVisible(True)
		self.BotonModoEliminar.setVisible(False)
		self.ApartadoTextpEjecutar.setVisible(False)
		self.ApartadoTextElegirModo.setVisible(False)
		self.ApartadoTextModoEliminar.setVisible(False)
		self.ApartadoTextpGrabar.setVisible(True)
		global grabarJson
		grabarJson = True	#& Se grabara el Json cuando se pulde el boton de iniciar
		self.botonIniciar.setText("Grabar")
		self.eliminarBloquesDerecha()
		secuenciasCargadas = False
		self.eliminarBloquesIzquierda()
		print("Preparado para Grabar Json ...")
		self.ApartadoIngresarNombre.setVisible(True)
		self.ApartadoIngresarTiempoDeRepeticion.setVisible(False)


	def TextoEjecutar(self) :
		self.botonIniciar.setVisible(True)
		self.BotonModoEliminar.setVisible(True)
		self.ApartadoTextpEjecutar.setVisible(True)
		self.ApartadoTextModoEliminar.setVisible(False)
		self.ApartadoTextElegirModo.setVisible(False)
		self.ApartadoTextpGrabar.setVisible(False)
		self.estilizarScrollArea()
		self.TiempoIngresado.setText("1")

		global secuenciasCargadas
		
		if(secuenciasCargadas == False):
			self.IniciarBloques()

		secuenciasCargadas = True
		global grabarJson
		grabarJson = False	#& Se ejecutara/Creara (idk) cuando se pulse el boton de iniciar
		self.botonIniciar.setText("Ejecutar")
		print("Preparado para Ejecutar Json ...")
		self.ApartadoIngresarNombre.setVisible(False)
		self.ApartadoIngresarTiempoDeRepeticion.setVisible(True)


	def AgregarNuevoBloque(self):
		global grabarJson, NombreNuevaSecuencia

		self.IngresoDeNombre:QLineEdit = self.lineEdit
		NombreNuevaSecuencia = self.IngresoDeNombre.text() ###########################luego reviso esto para cambiarlo
		self.NombreNuevoBloque = self.IngresoDeNombre.text()
		self.nuevoBoton = QToolButton()
		self.nuevoBoton.setStyleSheet("""
	QToolButton {
		background: #00ABE4;
		color: #fff;
		font:bold;
		padding: 10px 20px;
		border: none;
		border-radius: 3px;
		min-width: 148px;
		min-height: 15px;
		max-width: 148px;
		max-height: 20px;
	}
	QToolButton:hover {
		background-color: #1280a4;
		color: white;
	}
""")


		if(self.NombreNuevoBloque == ""):
			time = datetime.now()
			NombreNuevaSecuencia = str((f"{time.minute}-{time.hour}_{time.day}-{time.month}-{time.year}"))
			self.NombreNuevoBloque = NombreNuevaSecuencia

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
		background: #00ABE4;
		color: #fff;
		font:bold;
		padding: 10px 20px;
		border: none;
		border-radius: 5px;
		min-width: 420px;
		min-height: 30px;
		max-width: 420px;
		max-height: 30px;
	}
	QToolButton:hover {
		background-color: #1280a4;
		color: white;
	}
""")		
		

		if(grabarJson == False):
			self.nuevoBoton.setText(boton.text())
			self.layoutDerecha.addWidget(self.nuevoBoton)
			print(f"Botón presionado: {self.nuevoBoton.text()}")
			self.botonSecuencia.clicked.connect(self.manejar_click)


	def establecerTiempoDeRepeticion(self, checked):
		global TiempoDeRepeticion
		texto: str = self.TiempoIngresado.text()
		if (texto == ""):
			texto = "1"
		if (checked):
			if self.sender() is self.radioButtonSegundos:
				TiempoDeRepeticion = int(texto)
				# Realizar acciones para la opción 1
			elif self.sender() is self.radioButtonHora :
				TiempoDeRepeticion = int(texto) * 3600
				# Realizar acciones para la opción 2
			elif self.sender() is self.radioButtonMinutos:
				TiempoDeRepeticion = int(texto) * 60
				# Realizar acciones para la opción 2


	def ejecucion(self):
		global TiempoDeRepeticion, enEjecucion
		if self.layoutDerecha.count() != 0 and self.TiempoIngresado.text() != "":
			self.showMinimized()
			while enEjecucion:
				for i in range(self.layoutDerecha.count()):
					print(f"ejecutando la Secuencia {self.layoutDerecha.itemAt(i).widget().text()}")
					ejecutar(self.layoutDerecha.itemAt(i).widget().text())
				time.sleep(TiempoDeRepeticion)
			self.Normalizar()	#& Final de Hilo
			print("Normalizado Ejecucion")


	def createThreadEjecucion(self):
		global hiloProcesoEjecucion
		self.startKeyListener()
		print("Llamado Creacion Hilo Ejecucion")
		self.Minimizar()
		hiloProcesoEjecucion = threading.Thread(target=self.ejecucion, name="HiloEjecutar")
		hiloProcesoEjecucion.start()

	def startKeyListener(self):
		print("Llamado StartKeyListener")
		global kListener, keyPressEjecutar, keyReleaseEjecutar
		kListener = pynputKey.Listener(on_press=keyPressEjecutar, on_release=keyReleaseEjecutar)
		kListener.start()

	def createThreadGrabar(self):
		global hiloProcesoGrabar
		print("Llamado Creacion Hilo Grabar")
		self.Minimizar()
		hiloProcesoGrabar = threading.Thread(target=grabar, name="HiloGrabado")
		hiloProcesoGrabar.start()


	def stopHiloEjecucion(self):
		print("Llamado StopKeyListener")
		global kListener, enEjecucion
		if kListener is not None:	#& Asegurarse que no sea nulo, pa evitar peos
			print("KeyDetenido")
			enEjecucion = False
			kListener.stop()
		kListener = None


	def BotonIniciar(self):
		global grabarJson, EnModoEliminaar, enEjecucion, enGrabado
		if(grabarJson):
			self.AgregarNuevoBloque()
			self.showMinimized()
			enGrabado = True
			self.createThreadGrabar()
			# self.TextoEjecutar()
		else:
			if(EnModoEliminaar == False):
				enEjecucion = True
				self.createThreadEjecucion()


	def estilizarScrollArea(self):
		self.scrollAreaIzquierda = self.scrollArea1
		self.ScrollVertical = self.scrollAreaIzquierda.verticalScrollBar()
		self.ScrollVertical.setStyleSheet("""
	QScrollBar:vertical{
		background:#C7C7C7;
		border-radius: 3px;
	}
""")
		self.ScrollHorizontal = self.scrollAreaIzquierda.horizontalScrollBar()
		self.ScrollHorizontal.setStyleSheet("""
	QScrollBar:horizontal{
		background:#C7C7C7;
		border-radius: 3px;
	}
""")

		self.scrollAreaDerecha = self.scrollArea2
		self.ScrollVerticalDerecha = self.scrollAreaDerecha.verticalScrollBar()
		self.ScrollVerticalDerecha.setStyleSheet("""
	QScrollBar:vertical{
		background:#C7C7C7;
		border-radius: 3px;
	}
""")
		self.ScrollHorizontalDerecha = self.scrollAreaDerecha.horizontalScrollBar()
		self.ScrollHorizontalDerecha.setStyleSheet("""
	QScrollBar:horizontal{
		background:#C7C7C7;
		border-radius: 3px;
	}
""")


	def IniciarBloques(self):
		secuenciasUsuario: list[str] = getJsons()
		for index, value in enumerate(secuenciasUsuario):
			self.botonSecuencia = QToolButton()
			self.botonSecuencia.setStyleSheet("""
	QToolButton {
		background: #00ABE4;
		color: #fff;
		font-weight: bold;
		padding: 10px 20px;
		border: none;
		border-radius: 3px;
		min-width: 148px;
		min-height: 15px;
		max-width: 148px;
		max-height: 20px;
	}
	QToolButton:hover {
		background-color: #1280a4;
		color: white;
	}
""")
			self.layoutIzquierda.addWidget(self.botonSecuencia)
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