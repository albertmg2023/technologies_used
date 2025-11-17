import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QIcon # para dibujar
from PyQt5.QtCore import QSize, Qt # para acceder a constantes (colores)...
import re
from robotDrawer import RobotDrawer
from robot import Robot
import PyQt5.QtCore
class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.menu_widget = QListWidget()
        lista=["TONTO","GILIPOLLAS","IDIOTA","SUBNORMAL","GAY?"]
        for i in range(len(lista)):
            item = QListWidgetItem(lista[i])
            item.setTextAlignment(Qt.AlignCenter)
            self.menu_widget.addItem(item)

        self.text_widget = QLabel("Pulsa y te diré lo que eres")
        self.button = QPushButton("Pulsa aquí")
        self.button.clicked.connect(self.pulsadoboton)
        

        content_layout = QVBoxLayout()
        content_layout.addWidget(self.text_widget)
        content_layout.addWidget(self.button)
        main_widget = QWidget()
        main_widget.setLayout(content_layout)

        layout = QHBoxLayout()
        layout.addWidget(self.menu_widget, 1)
        layout.addWidget(main_widget, 4)
        self.setLayout(layout)
    def pulsadoboton(self):
        itemactual=self.menu_widget.currentItem()
        texto=itemactual.data(0)
        self.text_widget.setText(texto)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    with open("stylelayoutspract.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())