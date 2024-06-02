import time
from pynput.mouse import Listener, Button
import keyboard
from eventos import *

eventosDict: list[dict] = []
ejecutarJson = False	#& Pa diferenciar despues cuando andamos guardando o ejecutando la secuencia del Json


def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)

		writeJson("secuencia", eventosDict, 2)


def click(x: int, y: int, button: Button, pressed: bool):
	if pressed:
		global initialTime
		global tiempoPrevio

		tiempoActual: float = time.time() - initialTime
		diff : float = tiempoActual - tiempoPrevio	#& diferencia de tiempos
		print(f"actual: {tiempoActual:.6f} previo: {tiempoPrevio:.6f} diferencia {diff:.6f}")
		tiempoPrevio = tiempoActual


		if button == Button.middle:
			print("Botón medio presionado. Deteniendo el listener.")
			return False

		if button == Button.left or button == Button.right:
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : float(format(diff, ".3f")),
				"x": x,
				"y" : y
			})



print("Iniciado")
initialTime: float = time.time()
tiempoPrevio: float = 0.0

if not ejecutarJson:
	with Listener(on_click=click) as listener:
		print("Listener\n")
		listener.join()

	print("OutListener")

	keyboard.on_press(eventoTeclado)
	keyboard.wait("esc")