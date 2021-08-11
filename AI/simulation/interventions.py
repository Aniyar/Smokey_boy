import numpy as np


class Intervention:
    pass


class FireLine(Intervention):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def implement(self, X):
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
            for i in range(abs(dy) + 1):
                # Check if the x coordinate has changed - if so, plug holes
                x_new = int(np.round(x1 + i * dx / dy))
                if x_new != x_prev:
                    mask[y_start + i - 1: y_start + i + 1, x_new] = 0
                else:
                    mask[y_start + i, x_new] = 0
        else:
            # Calculate gradient wrt x
            x_start = min(x1, x2)
            y_prev = y1
            for i in range(abs(dx) + 1):
                y_new = int(np.round(y1 + i * dy / dx))
                if y_new != y_prev:
                    mask[y_new, x_start + i - 1: x_start + i + 1] = 0
                else:
                    mask[y_new, x_start + i] = 0
        X[3, :, :] = np.multiply(X[3, :, :], mask)
        return X


# - Fire fighters (needed for any other intervention to work)
# - Fireline (turns square in to square wil no fule)
# - Fire plane retardant (spews flame retardant, slows down how fast the flame spreads so will effect the effect this square has on others, has a lower chance of causing - those adjacent to it to go on fire)
# - Fire plane water (increases precipitation of the square)
# smoke jumper
# - Fire engain (increases precipitation of the square)
# - Bulldozer (can be used in place of human to change square to no fule)
# - Water (needed for fire hydrant to operate)
# - water tender

class TruckTeam():
    def __init__(self):
        self.neighbourhood = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                              (1, 0), (1, 1)]

    def step(self):
        x1, y1 = start
        x2, y2 = end
        time_sec = sqrt((20 * (max(x1, x2) - min(x1, x2)) ** 2) +
                        (20 * (max(y1, y2) - min(y1, y2)) ** 2)) / 27
        return time_sec

    def implement(self, end, X):
        x1, y1 = start
        x2, y2 = end
        self.Fighters -= self.En_fight
        precipitation = X[5, :, :]
        precipitation[y2, x2] = 0
        for n in range(self.neighbourhood):
            xn, yn = n
            precipitation[y2 + yn, x2 + xn] *= 2
        X[5, :, :] = precipitation
        return X
