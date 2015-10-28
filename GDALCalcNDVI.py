import sys,os,struct
from osgeo import gdal

class GDALCalcNDVI:
    
    def createOutputImage(self,outFilename, inDataset):
    
        driver = gdal.GetDriverByName("GTiff")
        metadata = driver.GetMetadata()
        if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
            print 'Driver GTiff supports Create() method.'
        else:
            print 'Driver GTiff does not support Create()'
            sys.exit(-1)
            
        geoTransform = inDataset.GetGeoTransform()
        geoProjection = inDataset.GetProjection()        
        newDataset = driver.Create(outFilename, inDataset.RasterXSize, inDataset.RasterYSize,1,gdal.GDT_Float32)
        newDataset.SetGeoTransform(geoTransform)
        newDataset.SetProjection(geoProjection)
        return newDataset  
        
    def calcNDVI(self,file,outFilePath):
    
        dataset = gdal.Open(file,gdal.GA_ReadOnly)
        if dataset is None:
            print "The dataset could not opened"
            sys.exit(-1)
            
        outDataset = self.createOutputImage(outFilePath,dataset)
        
        if outDataset is None:
            print 'Could not create output image'
            sys.exit(-1)
        
        red_band = dataset.GetRasterBand(3) # RED BAND
        nir_band = dataset.GetRasterBand(4) # NIR BAND
        
        numLines = red_band.YSize
        for line in range(numLines):
        
            outputLine = ''
            red_scanline = red_band.ReadRaster(0,line,red_band.XSize,1,red_band.XSize,1,gdal.GDT_Float32)
            red_tuple = struct.unpack('f'* red_band.XSize, red_scanline)
            
            nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize,1,nir_band.XSize,1,gdal.GDT_Float32)
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scanline)
            
            for i in range(len(red_tuple)):
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi = 0
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper/ndvi_lower
                outputLine = outputLine + struct.pack('f',ndvi)
            #print struct.unpack('f'*len(red_tuple),outputLine)
            outDataset.GetRasterBand(1).WriteRaster(0,line,red_band.XSize,1,outputLine,red_band.XSize,1,gdal.GDT_Float32)
            del outputLine
        
        print 'NVDI Calculated and Outputted to File'
            
if __name__ == '__main__':
    obj = GDALCalcNDVI()
    filePath="2015-07-24_195550_Russell-Small_Plots_West_NC.tif"
    outFilePath = "2015-07-24_195550_Russell-Small_Plots_West_NC_NDVI.tif"
    if os.path.exists(filePath):
        obj.calcNDVI(filePath,outFilePath)
    else:
        print 'The file does not exist.'
              