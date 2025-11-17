import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class CircleDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dibujar Círculo con Texto")
        self.setGeometry(100, 100, 400, 400)

        # Variables para almacenar los datos del círculo
        self.x = 0
        self.y = 0
        self.radius = 0
        self.text = ""

        # Layout
        layout = QVBoxLayout()

        # Campos de entrada
        self.x_input = QLineEdit(self)
        self.x_input.setPlaceholderText("Posición X")
        layout.addWidget(self.x_input)

        self.y_input = QLineEdit(self)
        self.y_input.setPlaceholderText("Posición Y")
        layout.addWidget(self.y_input)

        self.radius_input = QLineEdit(self)
        self.radius_input.setPlaceholderText("Radio")
        layout.addWidget(self.radius_input)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Texto")
        layout.addWidget(self.text_input)

        # Botón para dibujar
        self.draw_button = QPushButton("Dibujar Círculo", self)
        self.draw_button.clicked.connect(self.draw_circle)
        layout.addWidget(self.draw_button)

        # Establecer el layout
        self.setLayout(layout)

    def draw_circle(self):
        # Obtener los datos de entrada
        try:
            self.x = int(self.x_input.text())
            self.y = int(self.y_input.text())
            self.radius = int(self.radius_input.text())
            self.text = self.text_input.text()
            self.update()  # Forzar la actualización del widget
        except ValueError:
            # Manejar error de entrada no válida
            self.x_input.setText("Error")
            self.y_input.setText("Error")
            self.radius_input.setText("Error")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Para suavizar el círculo

        # Establecer el pincel y el borde
        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)

        # Dibujar el círculo
        painter.drawEllipse(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        # Dibujar el texto encima del círculo
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        
        text_rect = painter.boundingRect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2, Qt.AlignCenter, self.text)
        painter.drawText(text_rect, Qt.AlignCenter, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CircleDrawer()
    window.show()
    sys.exit(app.exec_())