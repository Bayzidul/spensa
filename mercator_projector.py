import math
import pdb
from gmap_const import GmapConst

class MercatorProjector:

  def __init__(self):
    self.pixel_origin = {"x":GmapConst.TILE_SIZE/2, "y":GmapConst.TILE_SIZE/2}
    self.pixels_per_lon_degree = GmapConst.TILE_SIZE/360.0
    self.pixels_per_lon_radian = GmapConst.TILE_SIZE/(2.0 * math.pi)

  def from_lat_lng_to_point(self, lat_lng):
    point_x = self.pixel_origin["x"] + float(lat_lng["longitude"]) * self.pixels_per_lon_degree
    siny = self.bound(math.sin( self.degrees_to_radians(float(lat_lng["latitude"]))), -0.9999, 0.9999 )
    point_y = self.pixel_origin["y"] + 0.5 * math.log((1.0 + siny) / (1.0 - siny )) * -self.pixels_per_lon_radian
    return {"x":point_x, "y":point_y}

  def from_point_to_lat_lng(self, point):
    lng = (point["x"] - self.pixel_origin["x"]) / self.pixels_per_lon_degree
    lat_radians = (point["y"] - self.pixel_origin["y"]) / -self.pixels_per_lon_radian
    lat = self.radians_to_degrees(2.0 * math.atan(math.exp(lat_radians)) - math.pi / 2.0)
    return {"latitude":lat, "longitude": lng}

  # protected

  def bound(self, value, opt_min=None, opt_max=None):
    if opt_min != None:
      value = max(value, opt_min)
    if opt_max != None:
      value = min(value, opt_max)
    return value

  def degrees_to_radians(self, deg):
    return deg * (math.pi / 180)

  def radians_to_degrees(self, rad):
    return rad / (math.pi / 180)
