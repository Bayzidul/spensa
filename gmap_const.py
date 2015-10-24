import math

class GmapConst:
  TILE_SIZE = 256

  def __init__(self):
    pass

  @classmethod
  def number_of_tiles(cls, zoom_level):
    return math.pow(2, zoom_level)
