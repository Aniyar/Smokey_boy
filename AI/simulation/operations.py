from .inventory import InventoryManager

class OperationsManager:
    def __init__(self, resources):
        self.inventory = InventoryManager(resources)
        self.interventions = {} # interventions associated with resources

    def request_intervention(self, intervention):
        """
        Creates an intervention if resources are availabe. Returns success.
        """
        allowed = self.inventory.request_resources(intervention.resources)
        if allowed:
            self.interventions[intervention] = intervention.resources
        return allowed
