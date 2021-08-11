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
