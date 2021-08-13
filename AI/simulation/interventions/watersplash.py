import numpy as np

from . import Intervention

# assuming that the precipitation layer is at X[5, :, :]
# still needs modification for the precipitation probability according to the equation
class WaterSplash(Intervention):
  def __init__(self, center, resources, splash_radius):
    super().__init__(resources)
    center = self.center
    splash_radius = self.splash_radius
    X = self.X
    precipitation_layer = X[5, :, :]

    y_bound, x_bound = precipitation_layer.shape
    x1, y1 = center

    x_start = x1 - splash_radius
    y_start = y1 - splash_radius
    
    for i in range((2 * splash_radius) + 1):
      for j in range((2 * splash_radius) + 1):
        if (y_start + j >= 0 and x_start + i >= 0) and (y_start + j < y_bound and x_start + i < x_bound):
          precipitation_layer[y_start + j, x_start + i] = round(np.random.random(), 1)
          
    X[5,:, :] = precipitation_layer
    return X
  
class FireTruckSplash(WaterSplash):
  def __init__(self, center, no_trucks):
    splash_radius = 3 * no_trucks
    super().__init__(center, {'firefighters': 5, 'firetruck': no_trucks}, splash_radius)

class ManualWaterSplash(WaterSplash):
  def __init__(self, center, no_firefighters):
    m = -0.0025 * (no_firefighters - 20)**2 + 1
    splash_radius =  m * no_firefighters if m * no_firefighters <= 26 else 0.9 * no_firefighters
    super().__init__(center, {'firefighters': no_firefighters}, round(splash_radius))

class HelicopterSplash(WaterSplash):
  def __init__(self, center):
    super().__init__(center, {'firefighters': 1,'helicopter': 1}, 5)

