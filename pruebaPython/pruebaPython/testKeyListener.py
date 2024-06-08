import keyboard
import pynput
import pyautogui as pgui

def keyPress(key: pynput.keyboard.Key):
	# print(key)
	print("Cant de Teclas Pulsadas Actualmente:", len(currentPress))
	currentPress.add(key)	#& Cada vez que se pulsa una tecla, se añade a las "teclas Actuales"

	if keyboard.is_pressed('0'):	#& Combinacion Simple para demostrar
		# pynput.keyboard.Controller().tap(key='a')
		for key in listaKeysCodes:
			print(key)
			controller.press(key)
			controller.release(key)

		controller.release('0')	#& misma tecla que se usa pa iniciar el if, si no es posible que se repita varias veces (el teclado detecta es cuando pulsamos, quizas si se pasa a liberar seria suficiente)
		listaKeys.clear()
		listaKeysCodes.clear()
		return

def keyRelease(key: pynput.keyboard.KeyCode):
	
	if len(currentPress) == 1:
		print("Released:", key)
		tecla = key.char if type(key) == pynput.keyboard.KeyCode else key.name
		listaKeys.append(tecla)
		listaKeysCodes.append(key)
		#& Aqui se deberia añadir a su accion
	else:
		teclas = [t.char if type(t) == pynput.keyboard.KeyCode else t.name for t in currentPress]
		keys = [t if type(t) == pynput.keyboard.KeyCode else t for t in currentPress]
		print("Pulsadas: ", teclas)
		#& Aqui se deberia añadir a su accion
		for index, tecla in enumerate(teclas):
			listaKeys.append(tecla)
			listaKeysCodes.append(keys[index])

	currentPress.clear()	#& Cada vez que se deja de pulsar, se limpia TODAS las letras actuales (Si es una combinacion, se pulsarian a la vez de todas formas)
	if key == pynput.keyboard.Key.esc:
		print("Listener Terminado, se solto la tecla:", key)
		return False


listaKeys: list[str] = []
listaKeysCodes: list[pynput.keyboard.Key | pynput.keyboard.KeyCode] = []
controller: pynput.keyboard.Controller = pynput.keyboard.Controller()
currentPress = set()
with pynput.keyboard.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
	keyListener.join()