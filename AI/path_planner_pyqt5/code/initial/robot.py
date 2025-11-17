from body import Body
from wheel import Wheel
import numpy as np

class Robot:
    def __init__(self, x,y,w,h,r):
        self.body = Body(x,y,w,h)
        self.front_wheel = Wheel([x,y],r)
        self.rear_wheel = Wheel([x+w,y],r)

    def get_front_wheel(self):
        return self.front_wheel
    
    def get_rear_wheel(self):
        return self.rear_wheel
    
    def get_body(self):
        return self.body
    def get_position(self):
        return self.get_body().get_pos()
    
    def set_wheel_size(self, r):
        self.front_wheel.set_radius(r)
        self.rear_wheel.set_radius(r)

    def get_wheel_size(self):
        return self.front_wheel.get_radius()
    
    def get_size(self):
        return self.body.get_size()
    
    def set_body_size(self,w=None,h=None):
        self.body.set_size(w,h)
        # update the rear wheel position accordingly
        new_x_rear_wheel = self.body.get_pos()[0]+w
        self.rear_wheel.set_pos(new_x_rear_wheel)
    def set_pos(self, x, y):
        """Actualizar posición del robot y las ruedas"""
        self.body.set_pos(x, y)  # Actualiza la posición del cuerpo
        self.front_wheel.set_pos(x, y)  # Actualiza la posición de la rueda delantera
        self.rear_wheel.set_pos(x + self.body.get_size()[0], y)  # Actualiza la rueda trasera