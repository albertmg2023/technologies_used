import numpy as np
class Body:
    def __init__(self,x,y,w,h):
        self.set_pos(x,y)
        self.set_size(w,h)
    
    def get_pos(self):
        return self.pos
    
    def get_size(self):
        return self.width, self.height
    
    def set_pos(self,x,y):

        self.pos = np.array([x,y])

    def set_size(self,w=None,h=None):
        if w is not None:
            self.width = w
        if h is not None:
            self.height = h