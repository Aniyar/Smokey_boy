from tqdm import tqdm 
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

from .simulation import step, init_del_loma_smol, OperationsManager

class SimulationManager:

    def __init__(self):
        pass

    def run_simulation(self, initial_state, interventions, steps=30, visualise=False):
        # Set up colormap
        colors = [(1, 0, 0, 0), (1, 1, 0, 1)]
        fire_cmap = LinearSegmentedColormap.from_list('fire_cmap', colors, N=10)
        # Init the inventory manager
        manager = OperationsManager({
            'bulldozer': 3
        })
        # Create interventions
        for intervention in interventions:
            success = manager.request_intervention(intervention)
            if not success:
                print('Out of resources!')
        # Run simulation
        if visualise:
            # Create animation
            fig = plt.figure(figsize=(25/3, 6.25));
            ax = fig.add_subplot(111)
            ax.set_axis_off()
            ims = []
        X = initial_state
        for i in tqdm(range(steps)):
            if visualise:
                fuel = X[3, :, :]
                burning = X[7, :, :]
                map_layer = ax.imshow(fuel, cmap='PiYG')
                fire_layer = ax.imshow(burning, cmap=fire_cmap)
                ims.append([map_layer, fire_layer])
            X = step(X)
            # Update with respect to interventions
            for inter in manager.interventions.keys():
                X = inter.step(X)
        if visualise:
            # Interval between frames (ms).
            anim = animation.ArtistAnimation(fig, ims, interval=100)
            plt.show()

        # Return the final state
        return X

if __name__ == '__main__':
    manager = SimulationManager()
    initial_state = init_del_loma_smol()
    initial_state[7, 150, 150] = 1
    manager.run_simulation(initial_state, [], visualise=True)