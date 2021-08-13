import numpy as np

from . import Intervention

# assuming that the precipitation layer is at X[5, :, :]
# still needs modification for the precipitation probability according to the equation
class WaterSplash(Intervention):
  def __init__(self, center, resources, splash_radius):
    super().__init__(resources)
    self.center = center
    self.splash_radius = splash_radius 
    
  def step(self, X):
    precipitation_layer = X[5, :, :]
    y_bound, x_bound = precipitation_layer.shape
    x1, y1 = self.center

    x_start = x1 - self.splash_radius
    y_start = y1 - self.splash_radius
    
    for i in range((2 * self.splash_radius) + 1):
      for j in range((2 * self.splash_radius) + 1):
        if (y_start + j >= 0 and x_start + i >= 0) and (y_start + j < y_bound and x_start + i < x_bound):
          precipitation_layer[y_start + j, x_start + i] = 30
          
    X[5,:, :] = precipitation_layer
    return X
  
class FireTruckSplash(WaterSplash):
  def __init__(self, center, no_trucks):
    splash_radius = 3 * no_trucks
    firefighter = 5 * no_trucks
    water = ((splash_radius * 2 + 1)**2) * no_trucks
    super().__init__(center, {'firefighter': firefighter, 'fire_engine': no_trucks, 'water': water}, splash_radius)

class ManualWaterSplash(WaterSplash):
  def __init__(self, center, no_firefighters):
    m = -0.0025 * (no_firefighters - 20)**2 + 1 if no_firefighters <= 26 else 0.9
    splash_radius =  round(m * no_firefighters)
    water = (splash_radius * 2 + 1)**2
    super().__init__(center, {'firefighter': no_firefighters, 'water': water}, round(splash_radius))

class HelicopterSplash(WaterSplash):
  def __init__(self, center):
    water = 100
    super().__init__(center, {'firefighter': 1,'fire_helicopter': 1, 'water': 100}, 5)