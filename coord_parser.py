import math
from gmap_const import GmapConst
from mercator_projector import MercatorProjector

class CoordConvertor:

 
    def latlngToWorldCoord(self,latlngUpperLeft,latlngDownRight):

        world_coord_upper_left = MercatorProjector().from_lat_lng_to_point(latlngUpperLeft) 
        world_coord_down_right = MercatorProjector().from_lat_lng_to_point(latlngDownRight)
        
        print "world_coord_upper_left: "+"x:"+str(world_coord_upper_left["x"])+"  y:"+str(world_coord_upper_left["y"])
        print "world_coord_down_right: "+"x:"+str(world_coord_down_right["x"])+"  y:"+str(world_coord_down_right["y"])
        
        return {"world_coord_upper_left":world_coord_upper_left,"world_coord_down_right":world_coord_down_right}
        
    def latlngToPixelCoord(self,latlngUpperLeft,latlngDownRight,zoom_level):
    	
        world_coord = self.latlngToWorldCoord(latlngUpperLeft,latlngDownRight)  
        world_coord_upper_left = world_coord["world_coord_upper_left"]
        world_coord_down_right = world_coord["world_coord_down_right"]
        pixel_coord_upper_left = { "x": math.floor(world_coord_upper_left["x"] * GmapConst.number_of_tiles(zoom_level)),
                    "y": math.floor(world_coord_upper_left["y"] * GmapConst.number_of_tiles(zoom_level))}
        pixel_coord_down_right = { "x": math.floor(world_coord_down_right["x"] * GmapConst.number_of_tiles(zoom_level)),
                    "y": math.floor(world_coord_down_right["y"] * GmapConst.number_of_tiles(zoom_level))}
        
        print "pixel_coord_upper_left: "+"x:"+str(pixel_coord_upper_left["x"])+"  y:"+str(pixel_coord_upper_left["y"])
        print "pixel_coord_down_right: "+"x:"+str(pixel_coord_down_right["x"])+"  y:"+str(pixel_coord_down_right["y"])
                    
        return {"pixel_coord_upper_left":pixel_coord_upper_left,"pixel_coord_down_right":pixel_coord_down_right}            
   
    	
    def pixelToTileCoord(self,pixel_coord_upper_left,pixel_coord_down_right):
                    
        tile_coord_upper_left = { "x": math.floor(pixel_coord_upper_left["x"] / GmapConst.TILE_SIZE),
                    "y": math.floor(pixel_coord_upper_left["y"] / GmapConst.TILE_SIZE) }
        tile_coord_down_right = { "x": math.floor(pixel_coord_down_right["x"] / GmapConst.TILE_SIZE),
                    "y": math.floor(pixel_coord_down_right["y"] / GmapConst.TILE_SIZE) }
	
        print "tile_coord_upper_left: "+"x:"+str(tile_coord_upper_left["x"])+"  y:"+str(tile_coord_upper_left["y"])
        print "tile_coord_down_right: "+"x:"+str(tile_coord_down_right["x"])+"  y:"+str(tile_coord_down_right["y"])
        
        return {"tile_coord_upper_left":tile_coord_upper_left,"tile_coord_down_right":tile_coord_down_right}
  
    def getPixelOffset(self,pixel_coord_upper_left):
       
        pixel_offset_x = pixel_coord_upper_left["x"] % GmapConst.TILE_SIZE

        pixel_offset_y = pixel_coord_upper_left["y"] % GmapConst.TILE_SIZE

        print "pixel_offset_x: "+ str(pixel_offset_x) + "  y:" + str(pixel_offset_y)
        return {"pixel_offset_x":pixel_offset_x,"pixel_offset_y":pixel_offset_y} 
