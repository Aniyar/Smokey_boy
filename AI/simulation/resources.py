class Resource:
    pass


class FireEngine(Resource):
    def __init__(self, start, En_water_cap, En_fight):
        self.En_fight = En_fight
        self.En_W_cap = En_water_cap
        self.start = start
        self.end = 0
        self.neighbourhood = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                             (1, 0), (1, 1)]

    def implement(self, end, X):
        x1, y1 = start
        x2, y2 = end
        time_mins = sqrt((20*(max(x1,x2)-min(x1,x2))**2)+(20*(max(y1,y2)-min(y1,y2))**2)) / 27
        self.Fighters -= self.En_fight
        precipitation = X[5, :, :]
        precipitation[y2, x2] = 0
        for n in range(self.neighbourhood):
            xn, yn = n
            precipitation[y2 + yn, x2 + xn] *= 2
        X[5, :, :] = precipitation
        return X