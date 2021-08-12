from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

from grid_init import init_del_loma_smol
from simulation import step
from interventions import BullDozedFireLine
from interventions import TruckTeam

if __name__ == '__main__':
    # Set up colormap
    colors = [(1, 0, 0, 0), (1, 1, 0, 1)]
    fire_cmap = LinearSegmentedColormap.from_list('fire_cmap', colors, N=10)

    # Init the grid
    X = init_del_loma_smol()

    # Init the interventions
    active_interventions = []

    # Start a fire at (150,150)
    X[7, 150, 150] = 1

    # Create a fireline
    fl = BullDozedFireLine((0, 150),(199, 140))
    active_interventions.append(fl)

    #send fire truck
    tk = TruckTeam((157,145), (157,145))
    active_interventions.append(tk)

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
        for inter in active_interventions:
            X = inter.step(X)

    # Interval between frames (ms).
    anim = animation.ArtistAnimation(fig, ims, interval=100)
    plt.show()
