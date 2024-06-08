#& Codigo Convertido de la Interfaz usando el comando "pyside6-uic -o [nombreArchivoResultante].py"


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaz.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
	QMetaObject, QObject, QPoint, QRect,
	QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
	QFont, QFontDatabase, QGradient, QIcon,
	QImage, QKeySequence, QLinearGradient, QPainter,
	QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
	QLabel, QSizePolicy, QToolButton, QWidget)

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		if not Dialog.objectName():
			Dialog.setObjectName(u"Dialog")
		Dialog.resize(815, 541)
		Dialog.setStyleSheet(u"QDialog{\n"
"	background: #25282D\n"
"}")
		self.frame = QFrame(Dialog)
		self.frame.setObjectName(u"frame")
		self.frame.setGeometry(QRect(10, 20, 251, 501))
		self.frame.setStyleSheet(u"QFrame{\n"
"	background: #313338;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QToolButton{\n"
"  background: #FF0043;\n"
"  color: #fff;\n"
"  padding: 10px 20px;\n"
"  border: none;\n"
"  border-radius: 5px;\n"
"    min-width: 70px;\n"
"    min-height: 10px;\n"
"    max-width: 70px;\n"
"    max-height: 10px;\n"
"\n"
" \n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #3e8e41;\n"
"}\n"
"")
		self.frame.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame.setFrameShadow(QFrame.Shadow.Raised)
		self.GRABAR = QToolButton(self.frame)
		self.GRABAR.setObjectName(u"GRABAR")
		self.GRABAR.setGeometry(QRect(130, 10, 110, 30))
		self.EJECUTAR = QToolButton(self.frame)
		self.EJECUTAR.setObjectName(u"EJECUTAR")
		self.EJECUTAR.setGeometry(QRect(10, 10, 110, 30))
		self.frame_6 = QFrame(self.frame)
		self.frame_6.setObjectName(u"frame_6")
		self.frame_6.setGeometry(QRect(10, 60, 231, 421))
		self.frame_6.setStyleSheet(u"QFrame{\n"
"	background: #313338;\n"
"}")
		self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
		self.frame_4 = QFrame(Dialog)
		self.frame_4.setObjectName(u"frame_4")
		self.frame_4.setGeometry(QRect(270, 0, 551, 541))
		self.frame_4.setStyleSheet(u"QFrame{\n"
"	border-radius:10px;\n"
"}")
		self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
		self.frame_2 = QFrame(self.frame_4)
		self.frame_2.setObjectName(u"frame_2")
		self.frame_2.setGeometry(QRect(10, 20, 521, 36))
		self.frame_2.setStyleSheet(u"QFrame{\n"
"	background: #313338;\n"
"	font-family:Helvetica;\n"
"	font-weight: bold;\n"
"}")
		self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
		self.horizontalLayout = QHBoxLayout(self.frame_2)
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.TextoDelApartado = QLabel(self.frame_2)
		self.TextoDelApartado.setObjectName(u"TextoDelApartado")
		self.TextoDelApartado.setStyleSheet(u"QLabel{\n"
"	  color: #fff;\n"
"}")

		self.horizontalLayout.addWidget(self.TextoDelApartado)

		self.NombreDelBloque = QFrame(self.frame_4)
		self.NombreDelBloque.setObjectName(u"NombreDelBloque")
		self.NombreDelBloque.setGeometry(QRect(10, 480, 521, 41))
		self.NombreDelBloque.setStyleSheet(u"QFrame{\n"
"	background: #35383F;\n"
"	font-family:Helvetica;\n"
"	font-weight: bold;\n"
"}")
		self.NombreDelBloque.setFrameShape(QFrame.Shape.StyledPanel)
		self.NombreDelBloque.setFrameShadow(QFrame.Shadow.Raised)
		self.label_2 = QLabel(self.NombreDelBloque)
		self.label_2.setObjectName(u"label_2")
		self.label_2.setGeometry(QRect(10, 10, 141, 16))
		self.label_2.setStyleSheet(u"QLabel{\n"
"	  color: #fff;\n"
"}")
		self.INICIAR = QToolButton(self.NombreDelBloque)
		self.INICIAR.setObjectName(u"INICIAR")
		self.INICIAR.setGeometry(QRect(400, 0, 110, 41))
		self.INICIAR.setStyleSheet(u"QToolButton{\n"
"  background: #FF0043;\n"
"  color: #fff;\n"
"  padding: 10px 20px;\n"
"  border: none;\n"
"  border-radius: 5px;\n"
"\n"
"\n"
" \n"
"}")
		self.frame_5 = QFrame(self.frame_4)
		self.frame_5.setObjectName(u"frame_5")
		self.frame_5.setGeometry(QRect(10, 60, 521, 411))
		self.frame_5.setStyleSheet(u"QFrame{\n"
"	background: #35383F\n"
"}")
		self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
		self.frame_5.setFrameShadow(QFrame.Shadow.Raised)

		self.retranslateUi(Dialog)

		QMetaObject.connectSlotsByName(Dialog)
	# setupUi

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
		self.GRABAR.setText(QCoreApplication.translate("Dialog", u"Grabar", None))
		self.EJECUTAR.setText(QCoreApplication.translate("Dialog", u"Ejecutar", None))
		self.TextoDelApartado.setText(QCoreApplication.translate("Dialog", u"Grabe o seleccione una Secuencia para ser mostrada ", None))
		self.label_2.setText(QCoreApplication.translate("Dialog", u"Nombre del bloque: ", None))
		self.INICIAR.setText(QCoreApplication.translate("Dialog", u"boton inicar", None))
	# retranslateUi

