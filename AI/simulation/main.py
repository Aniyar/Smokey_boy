from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

from grid_init import init_del_loma_smol
from simulation import step
from interventions import BullDozedFireLine
from operations import OperationsManager

if __name__ == '__main__':
    # Set up colormap
    colors = [(1, 0, 0, 0), (1, 1, 0, 1)]
    fire_cmap = LinearSegmentedColormap.from_list('fire_cmap', colors, N=10)

    # Init the grid
    X = init_del_loma_smol()

    # Init the inventory manager
    manager = OperationsManager({
        'bulldozer': 3
    })

    # Start a fire at (150,150)
    X[7, 150, 150] = 1

    # Create a fireline
    for i in range(10):
        fl = BullDozedFireLine((10 * i, 150),(199, 140))
        manager.request_intervention(fl)

    # Create animation
    fig = plt.figure(figsize=(25/3, 6.25));
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    ims = []

    for i in tqdm(range(30)):
        fuel = X[3, :, :]
        burning = X[7, :, :]
        map_layer = ax.imshow(fuel, cmap='PiYG')
        fire_layer = ax.imshow(burning, cmap=fire_cmap)
        ims.append([map_layer, fire_layer])
        X = step(X)
        # Update with respect to interventions
        for inter in manager.interventions.keys():
            X = inter.step(X)

    # Interval between frames (ms).
    anim = animation.ArtistAnimation(fig, ims, interval=100)
    plt.show()
