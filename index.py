import time
from pynput.mouse import Listener, Button
import json as js
import pyautogui
import keyboard

eventosDict: list[dict] = []

def eventoTeclado(tecla):
	if keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl") and tecla.name == "k":

		callEventos(eventosDict)

		json = js.dumps(eventosDict, indent=2)
		with open("./secuence.json", "w") as j:
			j.write(json)



def callEventos(diccionario: list[dict]):
	for index, evento in enumerate(diccionario):
		time.sleep(evento.get("timeSince"))
		eventName: str = evento.get("name")
		if eventName == "click_left" or eventName == "click_right":
			mouseClick(evento)
		print(evento)

def mouseClick(evento: dict):
	pyautogui.moveTo(evento.get("x"), evento.get("y"))
	eventName = evento.get("name")
	if eventName == "click_left":
		pyautogui.click
	else :
		pyautogui.rightClick()

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

with Listener(on_click=click) as listener:
	print("Listener\n")
	listener.join()

print("OutListener")

keyboard.on_press(eventoTeclado)
keyboard.wait("esc")
