""" 
Aqui se encuentran todos los eventos creados hasta el momento, y la funcion para llamarlos
"""

import time, pyautogui, json, pynput, os, re, threading

def callEventos(diccionario: list[dict]):
	"""
	Llama al evento correspondiente con el valor de su `name` y eseprara el tiempo indicado en su valor `timeSince` antes de llamar al evento
	
	esa funcion que llama es la que se encargara de realizar el evento como tal y el resto de sus valores
	"""
	for index, evento in enumerate(diccionario):
		print(f"\tSleep: {evento.get("timeSince")}")
		time.sleep(evento.get("timeSince"))
		eventName: str = evento.get("name")

		match eventName:
			case "mouseMove" | "startPos":
				mouseMove(evento)
			case "click_left" | "click_middle" | "click-right":
				mouseClick(evento)
			case "mouseDown":
				mouseDown(evento)
			case "mouseUp":
				mouseUp(evento)
			case "mouseScroll":
				mouseScroll(evento)
		print(f"\t\t|Evento{index}|: evento: {evento}")

def do_nothing():
	print("\t\t\t\t\t|did nothing")

def do_nothing():
	pass

def mouseMove(evento: dict):
	""" Mueve el Mouse a la Coordenada Enviada """
	pyautogui.moveTo(evento.get("x"), evento.get("y"))

def mouseClick(evento: dict):
	"""
	Hace click en la posicion actual del mouse
	"""
	eventName = evento.get("name")
	if eventName == "click_left":
		pyautogui.click()
	elif eventName == "click_right" :
		pyautogui.rightClick()
	elif eventName == "click_middle" :
		pyautogui.middleClick()

def mouseScroll(evento: dict):
	"""
	dx = Scroll Horitzontal al parecer
	dy = Hacia donde se hizo scroll (Menor a 0 es pa arriba, mayor pa abajo)
	"""
	control = pynput.mouse.Controller()
	pynput.mouse.Controller.scroll(control, evento.get("dx"), evento.get("dy"))
	del control

def mouseDown(evento: dict):
	control = pynput.mouse.Controller()
	boton: pynput.mouse.Button

	if(evento.get("button") == "left"):
		boton = pynput.mouse.Button.left
	elif(evento.get("button") == "middle"):
		boton = pynput.mouse.Button.middle
	elif(evento.get("button") == "right"):
		boton = pynput.mouse.Button.right
	pynput.mouse.Controller.press(control, boton)

	del control

def mouseUp(evento: dict):
	control = pynput.mouse.Controller()
	boton: pynput.mouse.Button

	if(evento.get("button") == "left"):
		boton = pynput.mouse.Button.left
	elif(evento.get("button") == "middle"):
		boton = pynput.mouse.Button.middle
	elif(evento.get("button") == "right"):
		boton = pynput.mouse.Button.right
	pynput.mouse.Controller.release(control, boton)

	del control

def writeJson(name: str, lista: list[dict], indentacion: int = 2):
	"""
	- `name` = Nombre a ponerle al archivo (para que el usuario pueda en un futuro nombrar sus propias secuencias)
	- `lista` = Lista con los diccionarios/Json para guardar en orden
	- `indentacion` = la indentacion que se le pone al Json cuando se crea, por default es `2`
	"""

	fileIn = json.dumps(lista, indent=indentacion)
	with open(f"./secuenciasUsuario/{name}.json", "w") as fileOut:
		fileOut.write(fileIn)

def readJson(name: str):
	"""
	- `name` = Path para abrir el Json, Path que empieza en el directorio del proyecto
	"""
	# TODO: Quizas como los Json solo seran de usuario, hacer que se lean solo de esa caprta ya en vez de la ruta del proyecto
	dicc: dict
	with open(f"./secuenciasUsuario/{name}.json", "r") as fileIn:
		dicc = json.load(fileIn)

	# print(dicc, "\n")
	return dicc	

def sortNumberNames(fileName):
	found = re.search(r"\d+", fileName)
	return int(found.group()) if found else 0

def getJsons(path: str = "./secuenciasUsuario") -> list[str]:
	#& el .json se podria eliminar de aqui si se desea
	listaFiles: list[str] = os.listdir(path)
	listaJsonNames: list[str] = [j for j in listaFiles if j.endswith(".json")]
	listaJsonNames = sorted(listaJsonNames, key=str.lower)
	listaJsonNames = sorted(listaJsonNames, key=sortNumberNames)
	return listaJsonNames

def deleteFile(path: str = "./secuenciasUsuario"):
	pass
	os.remove()
