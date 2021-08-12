class InventoryManager:

    def __init__(self, inventory):
        self.inventory = inventory  # {resource_code: count }


    def request_resources(self, resources):
        for key in resources:
            if self.inventory[key] - resources[key] < 0:
                return False

        for key in resources:
            self.inventory[key] -= resources[key]

        return True   
                # remove the resources that have just been allocated AND MAKE SURE THAT WE HAVE ENOUGH
        # self.resources -= intervention.resources
        # IF THERE IS A -ve NUMBER OF RESOURCES, DO NOT ALLOW THE ALLOCATION

    def free_resources(self, resources):
        pass

    # same thing but instead deallocate the resources and return to pool


# A CENSUS OF RESOURCES, IF / WHERE THE RESOURCES ARE ALLOCATED (i.e. which specific intervention), A FUNCTION TO ADD AN INTERVENTION TO THE LIST
