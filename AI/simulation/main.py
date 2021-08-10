import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

from grid_init import init_del_loma
from tqdm import tqdm


def step(X):
    """
  Grid layers

  1. Value [0,inf) - real [Done]
  2. Wind Speed [0,inf) - real [Done]
  3. Wind Direction [0,360) - real [Done]
  4. Fuel [0,1] - real [Done]
  5. Humidity [0, 100] - real [Done]
  6. Precipitation [0,inf) - real [Done]
  7. Altitude [0,inf) - real [Done]
  8. Burning {0,1} - boolean 
  9. road [0,1] - boolean
  10. Interventions [0, number of interventions] - discrete

  1 step = 7 seconds
  """
    ny, nx = X.shape[1:]
    # Current state
    wind_speed = X[1, :, :]
    wind_direction = X[2, :, :]
    fuel = X[3, :, :]
    humidity = X[4, :, :]
    precipitation = X[5, :, :]
    altitude = X[6, :, :]
    burning = X[7, :, :]
    # Probability that there will be a fire
    prob = np.zeros((ny, nx))
    neighbourhood = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                     (1, 0), (1, 1)]
    for y in range(1, ny - 1):
        for x in range(1, nx - 1):
            for neighbour in neighbourhood:
                dx, dy = neighbour
                neighbour_on_fire = burning[y + dy, x + dx]
                if neighbour_on_fire == 1:
                    # Slightly lower probability increase if the burning neighbour is diagnonal
                    probability_multiplier = 1.5 if np.abs(dy) + np.abs(
                        dx) < 2 else 1.2
                    # Increase the probability of burning
                    prob[y, x] = np.clip(
                        max(burning[y, x] * probability_multiplier,
                            fuel[y, x]), 0, 1)
            # Some stuff that will change the probabilities
            pass
    # Compute the new state
    new_burning = np.zeros((ny, nx))
    for y in range(ny):
        for x in range(nx):
            new_burning[y, x] = 1 if np.random.random() < prob[y, x] else 0
    X[7, :, :] = new_burning
    return X


def show_animation_frame(X, fig):
    ax = fig.gca()
    fuel = X[3, :, :]
    burning = X[7, :, :]
    ax.imshow(fuel, cmap='PRGn')
    ax.imshow(burning, cmap=fire_cmap)


if __name__ == '__main__':
    # Set up colormap
    colors = [(1, 0, 0, 0), (1, 1, 0, 1)]
    fire_cmap = LinearSegmentedColormap.from_list('fire_cmap', colors, N=10)

    # Init the grid
    X = init_del_loma()

    # Start a fire at (44,44)
    X[7, 44, 44] = 1

    fig = plt.figure(figsize=(25/3, 6.25))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    ims = []

    for i in tqdm(range(5)):
        fuel = X[3, :, :]
        burning = X[7, :, :] 
        map_layer = ax.imshow(fuel, cmap='PRGn')
        fire_layer = ax.imshow(burning, cmap=fire_cmap)
        ims.append([map_layer, fire_layer])
        X = step(X)

    # Interval between frames (ms).
    anim = animation.ArtistAnimation(fig, ims, interval=100)
    plt.show()
