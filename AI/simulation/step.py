import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
EMPTY, TREE, FIRE = 0, 1, 2
# Colours for visualization: brown for EMPTY, dark green for TREE and orange
# for FIRE. Note that for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)

# Grid dimensions in 20m resolution
nx, ny = 400, 400
grid = np.zeros((10, ny, nx))
# The initial fraction of the forest occupied by trees.
forest_fraction = 0.4
# Initialize the forest grid.
grid[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
grid[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < forest_fraction
# Display the grid
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(grid, cmap=cmap, norm=norm)#, interpolation='nearest')


# Grid Object with an example
class GridObject():
  def __init__(self, name, location, value):
    self.name = name
    self.location = location 
    self.value = value

hospital = GridObject("Hospital", grid[30:40, 30:40], 1000)

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
9. Roads {0,1} - boolean
10. Interventions [0, number of nterventions] - discrete
"""
# Properties for each pixel
class Weather():
  def __init__(self, windSpeed, windDir, humidity, temperature, precipitation, altitude, accessibility, interventions):
    self.windSpeed = windSpeed
    self.windDir = windDir
    self.humidity = humidity
    self.temp = temperature
    self.prec = precipitation
    self.altitude = altitude
    self.accessibility = accessibility
    self.interventions = interventions

    self.burnability = abs(self.windSpeed*(1/self.humidity)*self.temperature*(1/self.prec) - self.accessibility - self.interventions)
    
    if self.burnability >= 0.5:
      self.burning = True
    else:
      self.burning = False

# Updates the grid
def step(X):

  X1 = np.zeros((ny, nx))
  for ix in range(1,nx-1):
      for iy in range(1,ny-1):
          X[iy, ix] = Weather(np.random.rand()*100, np.random.rand() * 360, np.random.rand() * 100, np.random.rand() * 100, np.random.rand() * 1000, np.random.rand(), np.random.randint(0, 10))
          if X[iy,ix] == TREE:
              X1[iy,ix] = TREE
              for dx,dy in neighbourhood:
                  # The diagonally-adjacent trees are further away, so
                  # only catch fire with a reduced probability:
                  if abs(dx) == abs(dy) and np.random.random() < 0.573:
                      continue
                  if X[iy+dy,ix+dx].burning:
                      X1[iy,ix] = FIRE
                      break
              else:
                  if  X[iy, ix].burning:
                      X1[iy,ix] = FIRE
  return X1





# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = step(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = grid

# Interval between frames (ms).
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=200)
plt.show()