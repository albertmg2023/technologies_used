import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from secundarywin import *
from robotDrawer import RobotDrawer
from robot import Robot

class MainWindow(QMainWindow):
    def create_robot(self):
        # Valores iniciales del robot
        x, y = 120, 120
        w, h = 60, 40
        r = 15
        self.robot = Robot(x, y, w, h, r)

    def create_drawer(self):
        self.drawRobot = RobotDrawer(self.robot, self)  # Asume que RobotDrawer se encarga del dibujo del robot

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana con Botones")
        self.setGeometry(600, 400)

        # Crear el layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()
        self.buttons = []
        nombresarriba = ["CREATE ROBOT", "POSITION", "OBSTACLE", "PLAN", "RUN", "VISUALIZE"]

        # Crear los botones y añadirlos al layout horizontal
        for i in range(6):
            button = QPushButton(nombresarriba[i])
            button_layout.addWidget(button)
            self.buttons.append(button)

        # Establecer márgenes y espaciado
        button_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        button_layout.setSpacing(10)  # Espaciado entre botones

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)

        # Añadir un widget de dibujo si es necesario
        # self.drawing_widget = DrawingWidget()  # Define esta clase si es necesaria
        # main_layout.addWidget(self.drawing_widget)

        # Establecer las conexiones de los botones
        self.buttons[0].clicked.connect(self.open_create_robot_win)
        self.buttons[1].clicked.connect(self.open_position_robot_win)
        self.buttons[2].clicked.connect(self.open_obstacle_win)
        self.buttons[3].clicked.connect(self.open_plan_win)

        # Inicializar robot y pintarlo
        self.create_robot()
        self.create_drawer()
        self.drawRobot.draw()  # Asume que RobotDrawer tiene un método draw para pintar el robot

        # Mostrar la ventana
        
        self.show()

    # Métodos para abrir ventanas secundarias
    def open_create_robot_win(self):
        self.create_robot_win = Create_robot_win()  # Asegúrate que esta clase esté definida
        self.create_robot_win.show()

    def open_position_robot_win(self):
        self.position_robot_win = Position_robot_win()  # Asegúrate que esta clase esté definida
        self.position_robot_win.show()

    def open_obstacle_win(self):
        self.obstacle_win = Obstacle_win()  # Asegúrate que esta clase esté definida
        self.obstacle_win.show()

    def open_plan_win(self):
        self.plan_win = Plan_win()  # Asegúrate que esta clase esté definida
        self.plan_win.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())