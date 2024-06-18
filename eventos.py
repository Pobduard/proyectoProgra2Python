""" 
Aqui se encuentran todos los eventos creados hasta el momento, y la funcion para llamarlos
"""

import time, pyautogui, json, pynput, os, re

keyStr: str | pynput.keyboard.Key | pynput.keyboard.KeyCode = ""

matches: dict[str, pynput.keyboard.Key] = {
	'left' : pynput.keyboard.Key.left,
	'right' : pynput.keyboard.Key.right,
	'up' : pynput.keyboard.Key.up,
	'down' : pynput.keyboard.Key.down,
	'tab' : pynput.keyboard.Key.tab,
	'caps_lock' : pynput.keyboard.Key.caps_lock,
	'shift' : pynput.keyboard.Key.shift,
	'shift_l' : pynput.keyboard.Key.shift_l,
	'shift_r' : pynput.keyboard.Key.shift_r,
	'ctrl' : pynput.keyboard.Key.ctrl,
	'ctrl_l' : pynput.keyboard.Key.ctrl_l,
	'ctrl_r' : pynput.keyboard.Key.ctrl_r,
	'alt' : pynput.keyboard.Key.alt,
	'alt_l' : pynput.keyboard.Key.alt_l,
	'alt_r' : pynput.keyboard.Key.alt_r,
	'alt_gr' : pynput.keyboard.Key.alt_gr,
	'space' : pynput.keyboard.Key.space,
	'home' : pynput.keyboard.Key.home,
	'page_up' : pynput.keyboard.Key.page_up,
	'page_down' : pynput.keyboard.Key.page_down,
	'end' : pynput.keyboard.Key.end,
	'enter' : pynput.keyboard.Key.enter,
	'insert' : pynput.keyboard.Key.insert,
	'backspace' : pynput.keyboard.Key.backspace,
	'cmd' : pynput.keyboard.Key.cmd,
	'cmd_l' : pynput.keyboard.Key.cmd_l,
	'cmd_r' : pynput.keyboard.Key.cmd_r,
	'delete' : pynput.keyboard.Key.delete,
	'print_screen' : pynput.keyboard.Key.print_screen,
	'scroll_lock' : pynput.keyboard.Key.scroll_lock,
	'f1' : pynput.keyboard.Key.f1,
	'f2' : pynput.keyboard.Key.f2,
	'f3' : pynput.keyboard.Key.f3,
	'f4' : pynput.keyboard.Key.f4,
	'f5' : pynput.keyboard.Key.f5,
	'f6' : pynput.keyboard.Key.f6,
	'f7' : pynput.keyboard.Key.f7,
	'f8' : pynput.keyboard.Key.f8,
	'f9' : pynput.keyboard.Key.f9,
	'f10' : pynput.keyboard.Key.f10,
	'f11' : pynput.keyboard.Key.f11,
	'f12' : pynput.keyboard.Key.f12,
	'f13' : pynput.keyboard.Key.f13,
	'f14' : pynput.keyboard.Key.f14,
	'f15' : pynput.keyboard.Key.f15,
	'f16' : pynput.keyboard.Key.f16,
	'f17' : pynput.keyboard.Key.f17,
	'f18' : pynput.keyboard.Key.f18,
	'f19' : pynput.keyboard.Key.f19,
	'f20' : pynput.keyboard.Key.f20,
	'f21' : pynput.keyboard.Key.f21,
	'f22' : pynput.keyboard.Key.f22,
	'f23' : pynput.keyboard.Key.f23,
	'f24' : pynput.keyboard.Key.f24,
	'menu' : pynput.keyboard.Key.menu,
	'media_volume_up' : pynput.keyboard.Key.media_volume_up,
	'media_volume_down' : pynput.keyboard.Key.media_volume_down,
	'media_volume_mute' : pynput.keyboard.Key.media_volume_mute,
	'media_next' : pynput.keyboard.Key.media_next,
	'media_previous' : pynput.keyboard.Key.media_previous,
	'media_play_pause' : pynput.keyboard.Key.media_play_pause,
	'pause' : pynput.keyboard.Key.pause,
	'num_lock' : pynput.keyboard.Key.num_lock,
	'\u0011' : 'q',
	'\u0017' : 'w',
	'\u0005' : 'e',
	'\u0012' : 'r',
	'\u0014' : 't',
	'\u0019' : 'y',
	'\u0015' : 'u',
	'\t' : 'i',
	'\u000f' : 'o',
	'\u0010' : 'p',
	'\u0001' : 'a',
	'\u0013' : 's',
	'\u0004' : 'd',
	'\u0006' : 'f',
	'\u0007' : 'g',
	'\b' : 'h',
	'\n' : 'j',
	'\u000b' : 'k',
	'\f' : 'l',
	'\u00f1' : 'ñ',
	'\u001a' : 'z',
	'\u0018' : 'x',
	'\u0003' : 'c',
	'\u0016' : 'v',
	'\u0002' : 'b',
	'\u000e' : 'n',
	'\r' : 'm'
}


def callEventos(diccionario: list[dict]):
	"""
	Llama al evento correspondiente con el valor de su `name` y eseprara el tiempo indicado en su valor `timeSince` antes de llamar al evento
	
	esa funcion que llama es la que se encargara de realizar el evento como tal y el resto de sus valores
	"""
	keyController = pynput.keyboard.Controller()
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
			case "keyPress":
				keyPress(evento, keyController)
			case "keyRelease":
				keyRelease(evento, keyController)
		print(f"\t\t|Evento{index}|: evento: {evento}")

	del keyController


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

def checkKeys():
	global matches, keyStr
	if keyStr in matches:
		keyStr = matches[keyStr]

def keyPress(evento: dict, keyController: pynput.keyboard.Controller):
	global keyStr
	keyStr = evento["key"]
	checkKeys()
	keyController.press(keyStr)
	keyStr = ""

def keyRelease(evento: dict, keyController: pynput.keyboard.Controller):
	global keyStr
	keyStr = evento["key"]
	checkKeys()
	keyController.release(keyStr)
	keyStr = ""

def writeJson(name: str, lista: list[dict], indentacion: int = 2):
	"""
	- `name` = Nombre a ponerle al archivo (para que el usuario pueda en un futuro nombrar sus propias secuencias)
	- `lista` = Lista con los diccionarios/Json para guardar en orden
	- `indentacion` = la indentacion que se le pone al Json cuando se crea, por default es `2`
	"""

	path: str = f"./secuenciasUsuario/{name}.json"
	fileIn = json.dumps(lista, indent=indentacion)
	if(os.path.exists(path)):	#& Si existia, eliminarlo y crear nuevo
		os.remove(path)
	with open(path, "w") as fileOut:
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
	os.remove(f"./secuenciasUsuario/{path}.json")