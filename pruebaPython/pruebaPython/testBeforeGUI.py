import keyboard
import pynput
import pyautogui

def keyPress(key: pynput.keyboard.Key):
	# print(key)
	global controller
	global listaKeys
	global listaKeysCodes
	global currentPress
	print("Cant de Teclas Pulsadas Actualmente:", len(currentPress))
	print("Press", key, type(key))
	if(key == pynput.keyboard.Key.ctrl or key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r):
		currentPress.add(key)
		return
	else:
		currentPress.add(key)	#& Cada vez que se pulsa una tecla, se añade a las "teclas Actuales"
		return

def keyRelease(key: pynput.keyboard.Key | pynput.keyboard.KeyCode):
	global listaKeys
	global listaKeysCodes
	global keyListener
	global currentPress

	if len(currentPress) == 1:
		print("Released:", key, type(key))
		tecla = key.char if (type(key) == pynput.keyboard.KeyCode) else (key.name)
		listaKeys.append(tecla)
		listaKeysCodes.append(key)
		#& Aqui se deberia añadir a su accion
	else:
		teclas2 = [t.name if type(t) == pynput.keyboard.Key else t.char for t in currentPress]
		# print("Pulsadas: ", teclas, "||||", teclas2)
		print("Pulsadas: ", teclas2)
		#& Aqui se deberia añadir a su accion
		for index, tecla in enumerate(teclas2):
			listaKeys.append(tecla)
			# listaKeysCodes.append(keys[index])

	currentPress.clear()	#& Cada vez que se deja de pulsar, se limpia TODAS las letras actuales (Si es una combinacion, se pulsarian a la vez de todas formas)
	if key == pynput.keyboard.Key.esc:
		print("Listener Terminado, se solto la tecla:", key)
		keyListener.stop()
		return False

print("Start")
listaKeys: list[str] = []
listaKeysCodes: list[pynput.keyboard.Key | pynput.keyboard.KeyCode] = []
controller: pynput.keyboard.Controller = pynput.keyboard.Controller()
currentPress: set[pynput.keyboard.Key] = set()
# keyListener = pynput.keyboard.Listener(on_press=keyPress, on_release=keyRelease)
# keyListener.start()
keyListener = pynput.keyboard.Listener(on_press=keyPress, on_release=keyRelease)
keyListener.start()
print("End")