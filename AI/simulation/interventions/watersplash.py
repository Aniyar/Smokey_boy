import numpy as np

# assuming that the precipitation layer is at X[5, :, :]
# still needs modification for the precipitation probability according to the equation
class WaterSplash():
  def __init__(self,center, radius, X, splasher):
    center = self.center
    radius = self.radius
    splasher = self.splasher
    X = self.X
    precipitation_layer = X[5, :, :]

    y_bound, x_bound = precipitation_layer.shape
    x1, y1 = center
    radius = radius

    x_start = x1 - radius
    y_start = y1 - radius

    switch 
    
    for i in range((2 * radius) + 1):
      for j in range((2 * radius) + 1):
        if (y_start + j >= 0 and x_start + i >= 0) and (y_start + j < y_bound and x_start + i < x_bound):
          precipitation_layer[y_start + j, x_start + i] = round(np.random.random(), 1)
          
    X[5,:, :] = precipitation_layer
    return X