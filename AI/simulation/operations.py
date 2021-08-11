class InventoryManager:

    def __init__(self, inventory):
        self.inventory = inventory  # {resource_code: count }
        self.intervention = {}  # {intervention : resources allocated to the intervention}


    def request_resources(self, intervention):
        for key in intervention.resources:
            self.inventory[key] -= intervention.resources[key]
            
                # remove the resources that have just been allocated AND MAKE SURE THAT WE HAVE ENOUGH
        # self.resources -= intervention.resources
        # IF THERE IS A -ve NUMBER OF RESOURCES, DO NOT ALLOW THE ALLOCATION

    def delete_intervention(self, intervention):
        for key in intervention.resources:
            self.inventory[key] += intervention.resources[key]

    # same thing but instead deallocate the resources and return to pool


# A CENSUS OF RESOURCES, IF / WHERE THE RESOURCES ARE ALLOCATED (i.e. which specific intervention), A FUNCTION TO ADD AN INTERVENTION TO THE LIST
if __name__ == '__main__':
    from interventions import FireLine
    im = InventoryManager({
        'bulldozer': 3
    })
    print("TEST")
    print(im.inventory)
    im.request_resources(FireLine((0,0), (2,2)))
    im.delete_intervention(FireLine((0,0), (2,2)))
    print(im.inventory)
