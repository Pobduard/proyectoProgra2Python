import threading, pynput, time
condition: bool = False
kListener: pynput.keyboard.Listener = None
hilo: threading.Thread

def keyPress(key: pynput.keyboard.Key):
	if key == pynput.keyboard.Key.esc:
		global condition
		condition = True
		print("Exit Listener . . .")

def keyRelease(key: pynput.keyboard.Key): 
	print(f"Released: {key}")

def doWork():
	global condition, kListener
	num: int = 0
	while not condition:
		print("Thread", num)
		time.sleep(10)
		num += 1
	#& LLega aqui caundo ya "termino" el hilo, sigue estando dentro del mismo, pero
	#& Al ser el final del ciclo del mismo, si lo mande a parar/terminar
	#& Se ejecutara 1 sola vez, aqui es cuando DE VERDAD puedo asegurar que se "termino"
	#& Ek hilo para modificar datos o funciones despues
	kListener.stop()
	print("Thread should have ended")

def main():
	global kListener, hilo
	kListener = pynput.keyboard.Listener(on_press=keyPress, on_release=keyRelease)
	kListener.name = "KeyListener"
	hilo = threading.Thread(target=doWork, name="Hilo")
	hilo.start()
	kListener.start()
	print("Hilo Empezado")

if __name__ == "__main__":
	main()