import numpy as np

from . import Intervention

class FireLine(Intervention):
    def __init__(self, start, end):
        super().__init__({'bulldozer': 1})
        self.start = start
        self.end = end
        self.i = 0

    def step(self, X):
        _, ny, nx = X.shape
        mask = np.ones((ny, nx))
        x1, y1 = self.start
        x2, y2 = self.end

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
                    mask[y_start + self.i - 1: y_start + self.i + 1, x_new] = 0
                else:
                    mask[y_start + self.i, x_new] = 0
        else:
            # Calculate gradient wrt x
            x_start = min(x1, x2)
            y_prev = y1
            if self.i < abs(dx) + 1:
                y_new = int(np.round(y1 + self.i * dy / dx))
                if y_new != y_prev:
                    mask[y_new, x_start + self.i - 1: x_start + self.i + 1] = 0
                else:
                    mask[y_new, x_start + self.i] = 0
        X[3, :, :] = np.multiply(X[3, :, :], mask)
        self.i += 1
        return X