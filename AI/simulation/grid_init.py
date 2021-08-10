import numpy as np
from PIL import Image

def init_del_loma():
  # Grid dimensions in 20m resolution
  nx, ny = 400, 400

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
  9. road {0,1} - boolean
  10. Interventions [0, number of interventions] - discrete
  """

  # ==== Init grid =====
  grid = np.zeros((10, ny, nx))

  # ===== Init value layer =====
  with Image.open('value.png') as im:
    value_layer = np.asarray(im)
    value_layer = value_layer[:, :, 1]
    grid[0,:,:] = value_layer

  # ====== Init wind layers =====
  wind_speed = np.ones((ny, nx)) * 5 # Uniform speed
  wind_direction = np.ones((ny, nx)) * 180 # Blowing East
  grid[1,:,:] = wind_speed
  grid[2,:,:] = wind_direction

  # ======= Init fuel layer =========
  with Image.open("vegetation.png") as im:
    fuel = np.asarray(im)[:, :, 1] / 255
    grid[3, :, :] = fuel 
    
  # ======= Init humidity layer ======
  humid = np.ones((nx, ny))*20
  grid[4,:,:] = humid

  # ===== Init precipitation layer ======
  precipitation = np.zeros((ny, nx))
  grid[5,:,:] = precipitation

  # ====== Init altitude layer ========

  height_scale = 5. # how many meters does an increase of 1 unit represent?
  # Load altitude map
  with Image.open('height.png') as im:
    im = im.convert('L')
    heightmap = np.asarray(im) * height_scale
    grid[6,:,:] = heightmap

  # ======= Init road layer =======
  with Image.open('roads.png') as im:
    road_layer = np.asarray(im)
    road_layer = road_layer[:, :, 1]
    grid[8,:,:] = road_layer

  return grid


def init_del_loma_smol():
  # Grid dimensions in 20m resolution
  nx, ny = 200, 200

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
  9. road {0,1} - boolean
  10. Interventions [0, number of interventions] - discrete
  """

  # ==== Init grid =====
  grid = np.zeros((10, ny, nx))

  # ===== Init value layer =====
  with Image.open('value.png') as im:
    value_layer = np.asarray(im)
    value_layer = value_layer[200:, 200:, 1]
    grid[0, :, :] = value_layer

  # ====== Init wind layers =====
  wind_speed = np.ones((ny, nx)) * 5  # Uniform speed
  wind_direction = np.ones((ny, nx)) * 45  # Blowing South
  grid[1, :, :] = wind_speed
  grid[2, :, :] = wind_direction

  # ======= Init fuel layer =========
  with Image.open("vegetation.png") as im:
    fuel = np.asarray(im)[200:, 200:, 1] / 255
    grid[3, :, :] = fuel

    # ======= Init humidity layer ======
  humid = np.ones((nx, ny)) * 20
  grid[4, :, :] = humid

  # ===== Init precipitation layer ======
  precipitation = np.zeros((ny, nx))
  grid[5, :, :] = precipitation

  # ====== Init altitude layer ========

  height_scale = 5.  # how many meters does an increase of 1 unit represent?
  # Load altitude map
  with Image.open('height.png') as im:
    im = im.convert('L')
    heightmap = np.asarray(im) * height_scale
    grid[6, :, :] = heightmap[200:, 200:]

  # ======= Init road layer =======
  with Image.open('roads.png') as im:
    road_layer = np.asarray(im)
    road_layer = road_layer[200:, 200:, 1]
    grid[8, :, :] = road_layer

  return grid

if __name__ == '__main__':
  init_del_loma_smol()

