class Wheel:
    def __init__(self, center, radius):
        self.center = center
        self.set_radius(radius)

    def get_center(self):
       return self.center
    
    def get_radius(self):
       return self.radius
    
    def set_radius(self,radius):
        self.radius = radius

    def set_pos(self,x_new=None, y_new=None):
        x, y = self.get_center()
        if x_new is not None:
            x = x_new
        if y_new is not None:
            y = y_new
        self.center = [x,y]