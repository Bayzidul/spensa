from osgeo import gdal
from osgeo import osr
import numpy as np

def getlatlng(file):
    ds = gdal.Open(file)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    gt = ds.GetGeoTransform()

    originX = gt[0]
    originY = gt[3]
    pixelWidth = gt[1]
    pixelHeight = gt[5]

    minx = originX
    miny = originY + cols*gt[4] + rows*pixelHeight
    maxx = gt[0] + cols*pixelWidth + rows*gt[2]
    maxy = originY

    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjectionRef())
    srsLatLong = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs,srsLatLong)

    (lonUL,latUL,holder) = ct.TransformPoint(minx,maxy)
    latLonUpperLeft = {"longitude":lonUL,"latitude":latUL}
    (lonDR,latDR,holder) = ct.TransformPoint(maxx,miny)
    latLonDownRight = {"longitude":lonDR,"latitude":latDR}
    
    print latLonUpperLeft

    return {"latLonUpperLeft":latLonUpperLeft,"latLonDownRight":latLonDownRight}

