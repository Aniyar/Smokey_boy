import numpy as np

from . import Intervention


class FireLine(Intervention):
    def __init__(self, start, end, speed, fuel_reduction, resources):
        super().__init__(resources)
        self.start = start
        self.end = end
        self.i = 0
        self.speed = speed
        self.fuel_reduction = fuel_reduction

    def step(self, X):
        _, ny, nx = X.shape
        mask = np.ones((ny, nx))
        x1, y1 = self.start
        x2, y2 = self.end
        fuel = 1 - self.fuel_reduction
        if fuel < 0:
            fuel = 0

        dy = y2 - y1
        dx = x2 - x1
        m = -1 if dx < 0 else 1
        n = -1 if dy < 0 else 1
        
            
        for j in range(self.speed):
            
            if abs(dy) > abs(dx):
                counter = n * self.i * self.speed + j
                # Calculate gradient wrt y
                y_start = y1
                x_prev = x1
                if abs(counter) < abs(dy) + 1:
                    # Check if the x coordinate has changed - if so, plug holes
                    x_new = int(np.round(x1 + counter * dx / dy))
                    if x_new != x_prev:
                        mask[y_start + counter - 1: y_start +
                             counter + 1, x_new] *= fuel
                    else:
                        mask[y_start + counter, x_new] *= fuel
            else:
                counter = m * self.i * self.speed + j
                # Calculate gradient wrt x
                x_start = x1
                y_prev = y1
                if abs(counter) < abs(dx) + 1:
                    y_new = int(np.round(y1 + counter * dy / dx))
                    if y_new != y_prev:
                        mask[y_new, x_start + counter -
                             1: x_start + counter + 1] *= fuel
                    else:
                        mask[y_new, x_start + counter] *= fuel
        X[3, :, :] = np.multiply(X[3, :, :], mask)
        self.i += 1
        return X


class BullDozedFireLine(FireLine):
    def __init__(self, start, end):
        super().__init__(start, end, 3, 1, {'bulldozer': 1})


class ManualFireLine(FireLine):
    def __init__(self, start, end, no_firefighters):
        m = -0.0025 * (no_firefighters - 20)**2 + 1 if no_firefighters <= 25 else 0.9
        speed = m * no_firefighters
        super().__init__(start, end, round(speed), 0.8, {'firefighter': no_firefighters})


class PlaneFireLine(FireLine):
    def __init__(self, start, end):
        super().__init__(start, end, 5, 0.5, {'fire_plane': 1, 'firefighter': 1, 'retardent': 7200})
