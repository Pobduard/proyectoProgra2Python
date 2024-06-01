import keyboard

def eventoTeclado(tecla):
    if tecla.name == "k" and keyboard.is_pressed("ctrl"):print("combinacion presionada")


keyboard.on_press(eventoTeclado)
keyboard.wait("esc")