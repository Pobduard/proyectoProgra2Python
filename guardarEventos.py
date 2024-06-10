import time, math
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

""" 
def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)
		writeJson("secuencia", eventosDict, 2)
"""

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
		writeJson("secuencia", eventosDict, 2)	#& Modificar Json
		print("Nuevo Json Guardado")
		# window.showNormal()
		# window.show()
		# window.update()
		# print("Start")
		# callEventos(eventosDict)	#& TODO: Se tiene que eliminar de aqui despues al tener el boton pa ejecutar
		# print("End")
		return


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


		self.IniciarBloques()
		self.show()

		self.botonGrabar.clicked.connect(self.TextoGrabar)
		self.botonEjecutar.clicked.connect(self.TextoEjecutar)
		#self.botonIniciar.clicked.connect(self.IniciarBoton)

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

	def manejar_click(self):
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
		self.nuevoBoton.setProperty("direccionDeLaSecuencia",boton.property("direccionDeLaSecuencia"))
		self.nuevoBoton.setText(boton.text())
		self.layoutDerecha.addWidget(self.nuevoBoton)
		direccion = boton.property("direccionDeLaSecuencia")
		print(f"Botón presionado: {direccion}")
		print(f"Botón presionado: {self.nuevoBoton.property("direccionDeLaSecuencia")}")


	def IniciarBloques(self):
		for i in range(1, 50):
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
			self.layoutIzquierda.addWidget(self.botonSecuencia)
			self.botonSecuencia.setFixedSize(QSize(220,60))
			self.botonSecuencia.setProperty("direccionDeLaSecuencia",f"secuencia{i}.json")
			self.botonSecuencia.setText(f"secuencia{i}")
			self.botonSecuencia.clicked.connect(self.manejar_click)

		global grabarJson
		if(grabarJson):
			grabar()
		else:
			ejecutar()


if __name__ == "__main__": #&name es una variable de python , contiene el nombre del script
							#& osea aqui preguntamos , si este script es el modulo principal
							#+ Asi es, y por eso metere la funcion "main" aqui
	main()
	# grabar()	#& Probando directamente los listener, sin nececidad de la GUI