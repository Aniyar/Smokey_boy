import numpy as np
class Intervention:
    pass

class FireLine(Intervention):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def implement(self, X):
        _, ny, nx = X.shape
        grid = np.ones((ny, nx))
        x1, y1 = self.start
        x2, y2 = self.end
        locations = [(x1, y1)]
        grid[y1, x1] = 0
        slope = (y2 - y1) / (x2 - x1)
        xs = min(x1, x2)
        for i in range(abs(x1 - x2) + 1):
            grid[int(y1 + i * slope), xs + i] = 0
        X[3,:, :] = np.multiply(X[3,:, :], grid)
        return X