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
		pyautogui.moveTo(evento.get("x"), evento.get("y"))
		if evento.get("name") == "click_left" :
			pyautogui.click
			time.sleep(evento.get("timeSince"))
		elif evento.get("name") == "click_right":
			pyautogui.rightClick()
		
		print(evento)


def click(x: int, y: int, button: Button, pressed: bool):
	if pressed:
		passedTime: float = time.time()
		actualTime: float = float(format(passedTime - initialTime, ".2f"))	#& Limitado a 2 decimales

		global eventTime
		print(eventTime)
		if eventTime == 0:
			eventTime = actualTime
		else:
			eventTime = float(format((actualTime - eventTime), ".2f"))

		print(f"Se hizo clic en la posición ({x}, {y}) con el {button} y tiempoGlobal {actualTime} tiempoDesdeAccion {eventTime:.2f}")
		if button == Button.middle:
			print("Botón medio presionado. Deteniendo el listener.")
			return False



		if button == Button.left or button == Button.right:
			eventosDict.append({
				"name" : f"click_{button.name}",
				"timeSince" : eventTime,
				"x": x,
				"y" : y
			})

print("Iniciado")

initialTime: float = time.time()
eventTime: float = 0
with Listener(on_click=click) as listener:
	listener.join()


keyboard.on_press(eventoTeclado)
keyboard.wait("esc")
