""" 
Aqui se encuentran todos los eventos creados hasta el momento, y la funcion para llamarlos
"""

import time, pyautogui, json

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

def writeJson(name: str, lista: list[dict], indentacion: int = 2):
	"""
	``name`` = Nombre a ponerle al archivo (para que el usuario pueda en un futuro nombrar sus propias secuencias)

	``lista`` = Lista con los diccionarios/Json para guardar en orden

	``indentacion`` = la indentacion que se le pone al Json cuando se crea, por default es ``2``
	"""

	fileIn = json.dumps(lista, indent=indentacion)
	with open(f"./{name}.json", "w") as fileOut:
		fileOut.write(fileIn)