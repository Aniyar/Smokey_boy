import numpy as np
from interventions import fireline

class Plane(fireline):
    def __init__(self):
        super().__init__({'Plane': 1,'Fighter':1,'Retardent' : 7200})
        

#plane intervention uses retardent that decreases f
    def step(self, X):
        _, ny, nx = X.shape
        #mask = np.ones((ny, nx))
        x1, y1 = self.start
        x2, y2 = self.end
        fule = X[3, :, :]
        dy = y2 - y1
        dx = x2 - x1

        if abs(dy) > abs(dx):
            # Calculate gradient wrt y
            y_start = min(y1, y2)
            x_prev = x1
            if self.i < abs(dy) + 1:
                # Check if the x coordinate has changed - if so, plug holes
                x_new = int(np.round(x1 + self.i * dx / dy))
                if x_new != x_prev:
                    fule[y_start + self.i - 1: y_start + self.i + 1, x_new] = np.clip(fule[y_start + self.i - 1: y_start + self.i + 1, x_new] - 0.4) #this value can be changed, i am just assuming it decreases fule by a half
                else:
                    fule[y_start + self.i, x_new] = np.clip(fule[y_start + self.i, x_new] - 0.4)
        else:
            # Calculate gradient wrt x
            x_start = min(x1, x2)
            y_prev = y1
            if self.i < abs(dx) + 1:
                y_new = int(np.round(y1 + self.i * dy / dx))
                if y_new != y_prev:
                    fule[y_new, x_start + self.i - 1: x_start + self.i + 1] = np.clip(fule[y_new, x_start + self.i - 1: x_start + self.i + 1] - 0.4)
                else:
                    fule[y_new, x_start + self.i] = np.clip(fule[y_new, x_start + self.i] - 0.4)
        X[3, :, :] = fule
        self.i += 1
        return X