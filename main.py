from coord_parser import CoordConvertor
from get_latlng import getlatlng
from PIL import Image
from gmap_const import GmapConst
import os
import shutil
from osgeo import gdal

def makeTiles(file,zoom,outdir):
    
    tile_size = GmapConst.TILE_SIZE

    latLonPairs = getlatlng(file)

    latLonUpperLeft = latLonPairs["latLonUpperLeft"]

    latLonDownRight = latLonPairs["latLonDownRight"]

    pixel_coord = CoordConvertor().latlngToPixelCoord(latLonUpperLeft,latLonDownRight,zoom)

    pixel_coord_upper_left = pixel_coord["pixel_coord_upper_left"]

    pixel_coord_down_right = pixel_coord["pixel_coord_down_right"]

    tile_coord = CoordConvertor().pixelToTileCoord(pixel_coord_upper_left,pixel_coord_down_right);

    tile_coord_upper_left = tile_coord["tile_coord_upper_left"]

    tile_coord_down_right = tile_coord["tile_coord_down_right"]

    tile_min_x = int(tile_coord_upper_left["x"])

    tile_min_y = int(tile_coord_upper_left["y"])

    tile_max_x = int(tile_coord_down_right["x"])

    tile_max_y = int(tile_coord_down_right["y"])

#the offset is a tuple with x meaning offset to the right of the upperleft tile corner and y meaning offset below that corner


    pixel_offset = CoordConvertor().getPixelOffset(pixel_coord_upper_left)

    pixel_offset_x = int(pixel_offset["pixel_offset_x"])

    pixel_offset_y = int(pixel_offset["pixel_offset_y"])
    
    file_NVDI = GDALCalcNDVI().calcNDVI(file)

    im_field = Image.open(file)

    bg_width = (tile_max_x-tile_min_x+1)*tile_size
    bg_height = (tile_max_y-tile_min_y+1)*tile_size

    im_field_width = int(pixel_coord_down_right["x"]-pixel_coord_upper_left["x"])+1
    im_field_height = int(pixel_coord_down_right["y"]-pixel_coord_upper_left["y"])+1

    im_background = Image.new("RGBA",(bg_width,bg_height),(255,255,255,0))
    im_field_new = im_field.resize((im_field_width,im_field_height))
    im_background.paste(im_field_new,(pixel_offset_x,pixel_offset_y))
   # im_background.show()

    for x in range(tile_min_x,tile_max_x+1):
        for y in range(tile_min_y , tile_max_y+1):
            left = (x-tile_min_x)*tile_size
            upper = (y-tile_min_y)*tile_size
            right = left+tile_size
            lower = upper+tile_size
            box = (left,upper,right,lower)
            region = im_background.crop(box)
            path = outdir+ "/tiles/"+str(zoom)+"/"+str(x)+"/"
            if not os.path.exists(path):
                os.makedirs(path)
            region.save(os.path.join(path,str(y)+"@2x.png"))

if __name__ == '__main__':
    for zoom in range(2,19):
        makeTiles("2015-07-24_195550_Russell-Small_Plots_West_NC.tif",zoom,os.getcwd())



#3 TODO: how to use mapbox to add layers 

