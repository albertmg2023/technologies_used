import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QLabel
from secundarywin import *
import re
from PyQt5.QtCore import pyqtSignal, QObject
from robotDrawer import RobotDrawer
from robot import Robot
from body import Body
from PyQt5.QtGui import QPainter, QPen,QBrush
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QDialog
from robot import Robot
from object import Object
from obstacle import Obstacle 
from potentialFieldPathPlanner import PotentialFieldPathPlanner
import numpy as np

class Comunicador(QObject):
    obstacles_uploaded=pyqtSignal(str)
def dibujaobjetoslista(lista):
        for i in range(len(lista)):
            print("OBj",i,": " ,lista[i].x," ",lista[i].y," ",lista[i].size,lista[i].name)

#VENTANA PRINCIPAL

class MainWindow(QMainWindow):

    

    def create_robot(self):

        # initial values
        x,y = 120,120
        w,h = 60, 40
        r = 15
        self.robot = Robot(x,y,w,h,r)
        #posicion inicial por defecto
        self.posinicio=self.robot.get_body().get_pos()
    def create_drawer(self):
        self.drawRobot = RobotDrawer(self.robot, self)
    
    def paintEvent(self, event):
        if(self.dibujar_robot==True):

            self.drawRobot.draw()
        if(self.dibujar_ini==True):

            self.dibujacirculo(self.posinix,self.posiniy,2,"inicio",Qt.red)
        if(self.dibujar_fin==True):

            self.dibujacirculo(self.posfinalx,self.posfinaly,2,"FIN",Qt.red)
        self.dibuja_obstaculos()
        self.dibujar_ruta()
    




    def __init__(self):

        super().__init__()
        ##variables que controlan si se dibuja o no los elementos
        self.dibujar_robot=False
        self.dibujar_ini=False
        self.dibujar_fin=False
        self.ruta_completada=False

        self.comunicador=Comunicador()
    
        self.setWindowTitle("Ventana con Botones")
        self.setGeometry(100, 100, 600, 400)
        
        # Crear un widget para la parte superior
        top_widget = QWidget(self)
        self.setMenuWidget(top_widget)  # Opcional, solo si necesitas menú en la parte superior

         # Layout principal
        main_layout = QVBoxLayout()
        

        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()
        self.buttons=[]
        nombresarriba=["CREATE ROBOT","POSITION","OBSTACLE","PLAN","RUN","VISUALIZE"]
        # Crear los botones y añadirlos al layout
        for i in range(0, 6):
            button = QPushButton(nombresarriba[i])
            button_layout.addWidget(button)
            self.buttons.append(button)


        # Establecer el layout de botones sin margen
        button_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        button_layout.setSpacing(0)  # Espaciado entre botones (ajusta según sea necesario)

        # Asignar el layout al widget superior
        top_widget.setLayout(button_layout)

        #AÑADO los botones al layout vertical
        main_layout.addLayout(button_layout)

       
        #CREO UN WIDGET PARA DIBUJAR DEBAJO DE LOS BOTONES
        #self.drawing_widget = DrawingWidget()
        #main_layout.addWidget(self.drawing_widget)




        
        self.buttons[0].clicked.connect(self.open_create_robot_win)
        self.buttons[1].clicked.connect(self.open_position_robot_win)
        self.buttons[2].clicked.connect(self.open_obstacle_win)
        self.buttons[3].clicked.connect(self.open_plan_win)
        self.buttons[4].clicked.connect(self.mostrar_ruta)
        self.buttons[5].clicked.connect(self.dibujar_ruta)

        

        #incializamos robot y lo pintamos
        self.create_robot()
        self.create_drawer()
        self.drawRobot.draw()
        #inicializamos posinicio
        self.posiniy=100
        self.posinix=100
        #inicializamos pos final
        self.posfinaly=300
        self.posfinalx=300

        self.obstacles=[]

        #inicializo planificador

        self.planificador=PotentialFieldPathPlanner(self.robot)
        
        

        self.show()
    def open_create_robot_win(self,mensaje):
        self.create_robot_win1 = Create_robot_win()
        self.create_robot_win1.saverobot_completed.connect(self.actualiza_robot)    
        self.create_robot_win1.show()
        
    def enviarseñal_obstacles_uploaded(self):
        self.comunicador.obstacles_uploaded.emit("se ha actualizado los obstaculos")
    def actualizar_obstacles_obstacles_win(self):
        self.obstacle_win.actualiza_lista_obstaculos_desplegable(self.obstacles)

    def actualiza_robot(self):
        self.robot=self.create_robot_win1.robot
        #posicion inicial por defecto
        self.posinicio=self.robot.get_body().get_pos()
        self.create_drawer()
        self.dibujar_robot=True
        self.drawRobot.draw()

        self.repaint()
        
    def open_position_robot_win(self,mensaje):
        self.position_robot_win = Position_robot_win()
        self.position_robot_win.save_pos_ini_completed.connect(self.actualiza_posini)
        self.position_robot_win.save_pos_final_completed.connect(self.actualiza_posfinal)

        self.position_robot_win.show()

    def dibujacirculo(self, x, y, radius, text,color):
        painter = QPainter(self)

        # Establecer el pincel y el borde
        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QPen(color, 3)
        painter.setPen(pen)

        # Dibujar el círculo
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

        # Dibujar el texto encima del círculo
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)

        # Aquí ajustamos la posición del texto
        text_y = y - radius - 20  # Mover el texto 20 unidades hacia arriba
        text_rect = painter.boundingRect(x - radius, text_y - radius, radius * 2, radius * 2, Qt.AlignCenter, text)
        
        # Dibujar el texto centrado en la nueva posición
        painter.drawText(text_rect, Qt.AlignCenter, text)
        painter.end()

    #falta meter los text labels para actualizar el valor de posini y posiniy
    def actualiza_posini(self):
    
        self.posinix=self.position_robot_win.posini_x
        self.posiniy=self.position_robot_win.posini_y
        self.robot.set_pos(self.posinix, self.posiniy)
       
        #self.drawRobot=RobotDrawer(self.robot,self)
        self.dibujar_ini=True
        self.drawRobot.draw()
        self.dibujacirculo(self.posinix,self.posiniy,2,"INICIO",Qt.red)
        self.repaint()
    def actualiza_posfinal(self):
    
        self.posfinalx=self.position_robot_win.posfinal_x
        self.posfinaly=self.position_robot_win.posfinal_y
        self.dibujar_fin=True
        self.dibujacirculo(self.posfinalx,self.posfinaly,2,"FIN",Qt.red)
        self.repaint()

    def open_obstacle_win(self):
        dibujaobjetoslista(self.obstacles)
        self.obstacle_win = obstacle_win(self.obstacles)
        self.obstacle_win.actualiza_lista_obstaculos_desplegable(self.obstacles)
        self.obstacle_win.close_completed.connect(self.actualiza_obstaculos)
        #print(self.obstacle_win.obstacles[0].x)
        self.obstacle_win.create_completed.connect(self.actualiza_obstaculos)
        self.obstacle_win.edit_completed.connect(self.actualiza_obstaculos)
        self.obstacle_win.delete_completed.connect(self.actualiza_obstaculos)
        self.obstacle_win.show()
    def actualiza_obstaculos(self):
        self.obstacles=self.obstacle_win.obstacles
    #para actualizar los obstaculos cuando se cierra la ventana en la ventana de despues

    #def actualiza_obs_desplegale(self)


    def dibuja_obstaculos(self):
        for i in range(len(self.obstacles)):
            x=self.obstacles[i].x
            y=self.obstacles[i].y
            radius=self.obstacles[i].size
            name=self.obstacles[i].name
            self.dibujacirculo(x,y,radius,name,Qt.blue)
            
    def open_plan_win(self):
        self.plan_win = plan_win()
        self.plan_win.plan_completed.connect(self.actualiza_planer)

        

        self.plan_win.show()
    def actualiza_planer(self):
        self.planificador.num_iters_max=self.plan_win.max_iterations
        self.planificador.attraction_factor=self.plan_win.attraction_factor
        self.planificador.influence_area=self.plan_win.influence_area
        self.planificador.repulsion_factor=self.plan_win.repulsion_factor
        self.planer_configurado=True
    def mostrar_ruta(self):
        #añadir lista de obstaculos actuales 
        for i in range(len(self.obstacles)):

            self.planificador.add_obstacle(self.obstacles[i])
        #añadir el robot al planificador
        self.planificador.set_robot(self.robot)
        #añadir la posición final que queremos
        self.planificador.set_goal_point(self.posfinalx,self.posfinaly)
        self.ruta=self.planificador.run()
        #variable que indica que se ha coseguido una ruta de inicio a final
        self.ruta_completada=True
        #for i in range(len(self.ruta)):
            #print(self.ruta[i])
        #print(self.ruta)
    def dibujar_ruta(self):
        self.update()
        if(self.ruta_completada):
            painter = QPainter(self)
            

            # Configuración del pincel
            pen = QPen(Qt.blue, 2)
            painter.setPen(pen)

            # Dibujar la ruta conectando los puntos
            for i in range(len(self.ruta) - 1):
                # Dibujar una línea entre el punto actual y el siguiente
                painter.drawLine(int(self.ruta[i][0]),int(self.ruta[i][1]),int(self.ruta[i + 1][0]),int(self.ruta[i+1][1]))

            # Dibujar círculos pequeños en cada punto
            pen.setColor(Qt.red)
            painter.setPen(pen)
            for punto in self.ruta:
                painter.drawEllipse(int(punto[0]),int(punto[1]), 5, 5)  # Dibuja un círculo de radio 5 en cada punto

            # Terminar el pintado
            painter.end()
        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())