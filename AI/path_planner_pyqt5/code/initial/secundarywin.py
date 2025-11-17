import sys
from PyQt5.QtWidgets import *
from robot import Robot
import turtle
from PyQt5.QtCore import pyqtSignal, QObject
from obstacle import Obstacle

class Create_robot_win(QWidget):
    saverobot_completed=pyqtSignal(str)
    def create_robot(self):

        # initial values
        x,y = 120,120
        w,h = 60, 40
        r = 15
        self.robot = Robot(x,y,w,h,r)
    def __init__(self):
        #super().__init__()
        QObject.__init__(self)
        self.setWindowTitle("Ventana con TextEdits")
        self.setGeometry(100, 100, 300, 400)
        self.create_robot()
        

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Crear 4 QTextEdit y añadirlos al layout
        self.text_edits = []
        self.labels=[]
        nombresarriba=["X","Y","Width","High","RadiusWheels","NAME(Optional)"]
        
        for i in range(len(nombresarriba)):
            label = QLabel(nombresarriba[i])
            text_edit = QTextEdit(self)
            text_edit.setFixedSize(70,30)
            layout.addWidget(label)
            layout.addWidget(text_edit)
            self.labels.append(label)
            self.text_edits.append(text_edit)

        # Crear un botón en la parte inferior
        submit_button = QPushButton("SAVE", self)
        submit_button2 = QPushButton("CANCEL", self)
        submit_button.clicked.connect(self.on_submit)
        submit_button2.clicked.connect(self.on_submitCancel)
        layout.addWidget(submit_button)
        layout.addWidget(submit_button2)

        # Establecer el layout en el widget
        self.setLayout(layout)
    #comprobar si ninguno es caracter vacio para que no crashee
    def on_submit(self):
        no_vacios=True
        i=0
        while(i<=4 and no_vacios):
            if(self.text_edits[i].toPlainText()==""):
                no_vacios=False
            i+=1

        if(no_vacios):
            self.x = int(self.text_edits[0].toPlainText())
            self.y = int(self.text_edits[1].toPlainText())
            self.w=int(self.text_edits[2].toPlainText())
            self.h=int(self.text_edits[3].toPlainText())
            self.r=int(self.text_edits[4].toPlainText())
            self.robot = Robot(self.x,self.y,self.w,self.h,self.r)
        self.saverobot_completed.emit("Guardado")
        self.close() 

    def on_submitCancel(self):
        self.close()


class Position_robot_win(QWidget):
    save_pos_ini_completed=pyqtSignal(str)
    save_pos_final_completed=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Position")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()

        # Crear 4 QTextEdit y añadirlos al layout
        self.text_edits = []
        self.labels=[]
        pos1=["X1","Y1"]
        pos2=["X2","Y2"]
        lab = QLabel("Initial Position")
        layout.addWidget(lab)
        for i in range(len(pos1)):
            label = QLabel(pos1[i])
            text_edit = QTextEdit(self)
            text_edit.setFixedSize(70,30)
            layout.addWidget(label)
            layout.addWidget(text_edit)
            self.labels.append(label)
            self.text_edits.append(text_edit)
        
        # Crear un botón en la parte inferior
        submit_button = QPushButton("SAVE", self)
        submit_button.clicked.connect(self.on_submitinit)
        layout.addWidget(submit_button)
        lab = QLabel("Final Position")
        layout.addWidget(lab)
        for i in range(len(pos2)):
            label = QLabel(pos2[i])
            text_edit = QTextEdit(self)
            text_edit.setFixedSize(70,30)
            layout.addWidget(label)
            layout.addWidget(text_edit)
            self.labels.append(label)
            self.text_edits.append(text_edit)

        # Crear un botón en la parte inferior
        submit_button2 = QPushButton("SAVE", self)
        submit_button2.clicked.connect(self.on_submitfinal)

        layout.addWidget(submit_button2)

        # Establecer el layout en el widget
        self.setLayout(layout)

    def on_submitinit(self):
        
        if(self.text_edits[0].toPlainText()!="" and self.text_edits[1].toPlainText()!=""):
        #X1
            self.posini_x=int(self.text_edits[0].toPlainText())
        #Y1
            self.posini_y=int(self.text_edits[1].toPlainText())
        else:
            self.posini_x=40
            self.posini_y=40
        self.save_pos_ini_completed.emit("ini_completado")


        
    def on_submitfinal(self):
        if(self.text_edits[2].toPlainText()!="" and self.text_edits[3].toPlainText()!=""):
        #X2
            self.posfinal_x=int(self.text_edits[2].toPlainText())
        #Y2
            self.posfinal_y=int(self.text_edits[3].toPlainText())
        else:
            self.posfinal_x=200
            self.posfinal_y=200

        self.save_pos_final_completed.emit("fin_completado")

def dibujaobjetoslista(lista):
        for i in range(len(lista)):
            print("OBj",i,": " ,lista[i].x," ",lista[i].y," ",lista[i].size,lista[i].name)
class obstacle_win(QWidget):

    #creo signals para los botones de obstacle_win
    create_completed=pyqtSignal(str)
    edit_completed=pyqtSignal(str)
    delete_completed=pyqtSignal(str)
    close_completed=pyqtSignal(str)
    def __init__(self,listaobstaculos):
        super().__init__()

        # Layout principal
        layout = QVBoxLayout()

        # Desplegable para seleccionar obstáculos creados
        self.obstacle_selector = QComboBox()
        layout.addWidget(QLabel("Select Obstacle:"))
        layout.addWidget(self.obstacle_selector)

        # Campos para ingresar datos del obstáculo
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.size_input = QLineEdit()
        self.name = QLineEdit()

        layout.addWidget(QLabel("X Position:"))
        layout.addWidget(self.x_input)
        layout.addWidget(QLabel("Y Position:"))
        layout.addWidget(self.y_input)
        layout.addWidget(QLabel("Size:"))
        layout.addWidget(self.size_input)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name)
        # Botones para crear, editar y borrar
        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_obstacle)
        button_layout.addWidget(self.create_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_obstacle)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_obstacle)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Establecer el layout principal
        self.setLayout(layout)

        # Inicializar lista de obstáculos
        self.obstacles=listaobstaculos
        dibujaobjetoslista(self.obstacles)
        self.actualiza_lista_obstaculos_desplegable(self.obstacles)

    def closeEvent(self, event):
        self.close_completed.emit("Window closed, obstacles updated")
        event.accept() 

    def create_obstacle(self):
        # Crear un nuevo obstáculo con los datos proporcionados
        x = int(self.x_input.text())
        y = int(self.y_input.text())
        size = int(self.size_input.text())
        name = self.name.text()

        # Añadir el obstáculo a la lista y al combo box ,se lama 1 para que no sea el mismo nombre que la clase
        obstacle1=Obstacle(x,y,size,name)
        obstacle_DESCRIPTION = f"Obstacle {name} (X: {x}, Y: {y}, Size: {size})"
        self.obstacles.append(obstacle1)
        self.obstacle_selector.addItem(obstacle_DESCRIPTION)

        # Limpiar campos
        self.x_input.clear()
        self.y_input.clear()
        self.size_input.clear()
        self.name.clear()
        self.create_completed.emit("create completado")
        self.close()
    def edit_obstacle(self):
        # Editar el obstáculo seleccionado
        current_index = self.obstacle_selector.currentIndex()
        if current_index >= 0:
            x = self.x_input.text()
            y = self.y_input.text()
            size = self.size_input.text()
            name=self.name.text()

            updated_obstacle = f"Obstacle {name} (X: {x}, Y: {y}, Size: {size})"
            self.obstacles[current_index] = Obstacle(x,y,size,name)
            self.obstacle_selector.setItemText(current_index, updated_obstacle)

            # Limpiar campos
            self.x_input.clear()
            self.y_input.clear()
            self.size_input.clear()
            self.name.clear()
        self.edit_completed.emit("edit copmpleted")

    def delete_obstacle(self):
        # Borrar el obstáculo seleccionado
        current_index = self.obstacle_selector.currentIndex()
        if current_index >= 0:
            self.obstacles.pop(current_index)
            self.obstacle_selector.removeItem(current_index)
        self.delete_completed.emit("deletecompletado")

    #para actualizar el desplegable con la listade obataculos que guarda la ventana principal 
    #cuando se cierra la ventana de obstacles
    def actualiza_lista_obstaculos_desplegable(self,lista_obs):
        self.obstacle_selector.clear()
        for i in range(len(lista_obs)):

            updated_obstacle = f"Obstacle {lista_obs[i].name} (X: {lista_obs[i].x}, Y: {lista_obs[i].y}, Size: {lista_obs[i].size})"
            self.obstacle_selector.addItem(updated_obstacle)


class plan_win(QWidget):
    plan_completed=pyqtSignal(str)
    def guardar_info_planer(self):
           
        if(self.inputs[0].toPlainText()!=""):
            self.max_iterations=int(self.inputs[0].toPlainText())
        if(self.inputs[1].toPlainText()!=""):
            self.influence_area=int(self.inputs[1].toPlainText())
        if(self.inputs[2].toPlainText()!=""):
            self.attraction_factor=int(self.inputs[2].toPlainText())
        if(self.inputs[3].toPlainText()!=""):
            self.repulsion_factor=int(self.inputs[3].toPlainText())

        #envio señal para que la ventana principal actualice sus parámetros del planer
        self.plan_completed.emit("plan_completed")
       
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parámetros de Configuración")
        self.setGeometry(100, 100, 400, 200)
        
        # Crear un layout vertical para la ventana secundaria
        layout = QVBoxLayout()

        # Lista de parámetros y sus etiquetas
        parametros = [
            ("Max Iterations", "max_iterations"),
            ("Influence Area", "influence_area"),
            ("Attraction Factor", "attraction_factor"),
            ("Repulsion Factor", "repulsion_factor")
        ]

        # Crear los campos de texto y etiquetas
        self.inputs = []
        for label_text, param_name in parametros:
            h_layout = QHBoxLayout()  # Layout horizontal para cada fila
            label = QLabel(label_text)
            input_field = QTextEdit()
            input_field.setFixedHeight(25)
            
            h_layout.addWidget(label)       # Añadir etiqueta
            h_layout.addWidget(input_field)  # Añadir campo de entrada
            
            layout.addLayout(h_layout)  # Añadir la fila al layout principal
            self.inputs.append(input_field)  # Guardar text_edits en una lista
        
        # Botón para guardar o aceptar los cambios
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.guardar_info_planer)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

       
                





