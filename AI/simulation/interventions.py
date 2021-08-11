import numpy as np
class Intervention:
    pass

class FireLine(Intervention):
    def __init__(self, start, end, thickness):
        self.start = start
        self.end = end
        self.thickness = thickness

    def implement(self, X):
        _, ny, nx = X.shape
        grid = np.ones((ny, nx))
        x1, y1 = self.start
        x2, y2 = self.end
        locations = [(x1, y1)]
        while(x1 != x2 or y1 != y2):
            if x1 != x2:
                x1 += 1
            if y1 != y2:
                y1 += 1
            #print("x1: {} | y1: {}".format(x1, y1))
            locations.append((x1, y1))
            
        for x, y in locations:
            grid[y, x] = 0
        
        return grid
    
fl = FireLine((0,0), (5, 5), 1)
print(fl.implement(np.zeros((1, 10, 10))))