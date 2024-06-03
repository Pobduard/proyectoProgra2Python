import time
from pynput import mouse, keyboard as pynputKey
import keyboard
from eventos import *

eventosDict: list[dict] = []
ejecutarJson = False	#& Pa diferenciar despues cuando andamos guardando o ejecutando la secuencia del Json


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

def keyPress():
	pass

def keyRelease():
	pass

print("Iniciado")
initialTime: float = time.time()
tiempoPrevio: float = 0.0

if not ejecutarJson:
	with mouse.Listener(on_click=mouseClick) as mouseListener, pynputKey.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
		mouseListener.join()
		keyListener.join()
	

	keyboard.on_press(eventoTeclado)
	keyboard.wait("esc")

else:
	dicc = readJson("secuence")
	callEventos(dicc)