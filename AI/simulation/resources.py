class Resource:
    def __init__(self, code):
        self.resource_code = code  # A unique id for the resource type


class FireEngine(Resource):
    def __init__(self, start, En_water_cap, En_fight):
        super('fire_engine')
        self.En_fight = En_fight
        self.En_W_cap = En_water_cap


class BullDozer(Resource):
    def __init__(self):
        super('bulldozer')


class FireFighter(Resource):
    def __init__(self, intervention):
        super('firefighter')
        self.intervention = intervention


class FirePlane(Resource):
    def __init__(self, retardant_v):
        super('fire_plane')
        self.retardant_v = retardant_v


class FireHelicopter(Resource):
    def __init__(self, water_v):
        super('fire_helicopter')
        self.water_v = water_v

class FireRetardant(Resource):
    def __init__(self, volume):
        super('retardant')
        self.volume = volume


class Water(Resource):
    def __init__(self, volume):
        super('water')
        self.volume = volume