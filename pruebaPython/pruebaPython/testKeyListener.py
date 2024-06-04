import keyboard
import pynput


def keyPress(key: pynput.keyboard.Key):
	# print(key)
	print("Cant de Teclas Pulsadas Actualmente:", len(currentPress))
	currentPress.add(key)	#& Cada vez que se pulsa una tecla, se añade a las "teclas Actuales"

def keyRelease(key: pynput.keyboard.KeyCode):
	
	if len(currentPress) == 1:
		print("Released:", key)
		#& Aqui se deberia añadir a su accion
	else:
		teclas = [t.char if type(t) == pynput.keyboard.KeyCode else t.name for t in currentPress]
		print("Pulsadas: ", teclas)

	currentPress.clear()	#& Cada vez que se deja de pulsar, se limpia TODAS las letras actuales (Si es una combinacion, se pulsarian a la vez de todas formas)
	if key == pynput.keyboard.Key.esc:
		print("Listener Terminado, se solto la tecla:", key)
		return False



currentPress = set()
with pynput.keyboard.Listener(on_press=keyPress, on_release=keyRelease) as keyListener:
	keyListener.join()