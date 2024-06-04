import sys
from PyQt6 import uic #importar lo necesario para las interfaces graficas
from PyQt6.QtWidgets import * # importar todos los widgets de la interfaz grafica

class pantalla(QDialog):
    def __init__(self):
        super(pantalla, self).__init__()
        uic.loadUi("interfaz.ui", self)
        self.setWindowTitle("mas nunca en mi vida usare python")
        self.frames = []


        self.GRABAR.clicked.connect(self.TextoGrabar)
        self.EJECUTAR.clicked.connect(self.TextoEjecutar)

    def TextoGrabar(self) :
        self.TextoDelApartado.setText("Grabe o seleccione una secuencia para ser mostrada.")

    def TextoEjecutar(self) :
        self.TextoDelApartado.setText("Secuencia:")    

if __name__ == "__main__": #name es una variable de python , contiene el nombre del script
                            # osea aqui preguntamos , si este script es el modulo principal
    app = QApplication(sys.argv)
    dia = pantalla()
    dia.show()
    sys.exit(app.exec())                            
