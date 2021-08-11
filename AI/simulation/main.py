import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

from grid_init import init_del_loma_smol
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
    # Probability multipliers (initialised to -1)
    prob_multipliers = np.ones((ny, nx)) * -1
    for y in range(1, ny - 1):
        for x in range(1, nx - 1):
            neighbourhood = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                             (1, 0), (1, 1)]
            if burning[y, x] == 1:
                # If we are already burning...
                # Simulate the impact of embers flying off and starting more fires far away
                if np.random.random() < 0.002:
                    # The distance the ember travels
                    distance = int(wind_speed[y, x] * 1.5)
                    # Calculate the displacement assuming the ember travels with the wind
                    wind_direction_rad = np.radians(wind_direction[y, x])
                    dy = int(distance * - np.cos(wind_direction_rad))
                    dx = int(distance * np.sin(wind_direction_rad))
                    # Stay within grid bounds
                    if y + dy in range(ny) and x + dx in range(nx):
                        # Let the ember land on the ground and potentially start a fire.
                        prob_multipliers[y + dy, x + dx] = 5
            else:
                # If we are not burning, check if we should burn
                for neighbour in neighbourhood:
                    dx, dy = neighbour
                    neighbour_on_fire = burning[y + dy, x + dx]
                    if neighbour_on_fire == 1:
                        if prob_multipliers[y, x] == -1:
                            prob_multipliers[y, x] = 1
                        # Slightly lower probability increase if the burning neighbour is diagnonal
                        prob_multipliers[y, x] *= 1 if np.abs(dy) + np.abs(
                            dx) < 2 else 0.7

                        # Wind impact
                        prob_multipliers[y, x] *= 1 + np.dot(
                            [-dy, -dx]/np.linalg.norm(neighbour),
                            [
                                -np.cos(np.radians(wind_direction[y + dy, x + dx])),
                                np.sin(np.radians(
                                    wind_direction[y + dy, x + dx]))
                            ]
                        )
                        prob_multipliers[y, x] *= (1 + wind_speed[y, x])/20

                        # Slope
                        m = (altitude[y, x] - altitude[y+dy, x+dx]) / \
                            (np.abs(np.linalg.norm(neighbour)) * 10)
                        prob_multipliers[y, x] *= (1+m) if m > 0 else (1/(1-m))

                        # Road
                        # d = np.linalg.norm((y, x)-(y+dy, x+dx)) if road_layer[y + dy, x + dx] == 1 else

                # Humidity
    prob_multipliers *= 1 / (1 + 0.007 * humidity)
    # Compute the probability of burning
    prob = np.maximum(
        np.clip(np.multiply(fuel, prob_multipliers), 0, 1),
        burning
    )
    # Compute the new state by sampling probabilities at each cell
    new_burning = np.zeros((ny, nx))
    random_matrix = np.random.random((ny, nx))
    new_burning = (random_matrix < prob).astype(float)
    X[7, :, :] = new_burning
    return X


if __name__ == '__main__':
    # Set up colormap
    colors = [(1, 0, 0, 0), (1, 1, 0, 1)]
    fire_cmap = LinearSegmentedColormap.from_list('fire_cmap', colors, N=10)

    # Init the grid
    X = init_del_loma_smol()

    # Start a fire at (44,44)
    X[7, 150, 150] = 1

    fig = plt.figure(figsize=(25/3, 6.25))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    ims = []

    for i in tqdm(range(30)):
        fuel = X[6, :, :]
        burning = X[7, :, :]
        map_layer = ax.imshow(fuel, cmap='jet')
        fire_layer = ax.imshow(burning, cmap=fire_cmap)
        ims.append([map_layer, fire_layer])
        X = step(X)

    # Interval between frames (ms).
    anim = animation.ArtistAnimation(fig, ims, interval=100)
    plt.show()
