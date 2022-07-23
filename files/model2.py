#En este script utilizamos el raster suit/hdr.adf para crear un archivo .tif con la calidade de la tierra

# Definimos las rutas para los inputs y los outputs del modelo

mainpath = "/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4"
suitin = "{}/suit/suit/hdr.adf".format(mainpath)
outpath = "{}/_output/".format(mainpath)
suitout = "{}/landquality.tif".format(outpath)   

       
##################################################################
# Warp (reproject), definido como WGS 84 SR
##################################################################

# a) A partir de la layer, usamos la funcion de reproject 
        warp_dict = {
            'DATA_TYPE': 0,  # Usar el tipo de datos de la capa de entrada
            'EXTRA': '',
            'INPUT': suitin,
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Vecino más próximo
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        outputs['CombarReproyectar'] = processing.run('gdal:warpreproject', warp_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['Suitout']['OUTPUT']

 
##################################################################
# Extract projection
##################################################################

# b) Usamos esta funcion para que nos guarde el tipo de project que tiene
        extr_proj = {
            'INPUT': outputs['Suitout']['OUTPUT'],
            'PRJ_FILE_CREATE': False
        }
        outputs['ExtraerProyeccion'] = processing.run('gdal:extractprojection', extr_proj, context=context, feedback=feedback, is_child_algorithm=True)
 
    
##################################################################
# Save
##################################################################
# c) guardamos el archivo .tif

extpr_dict = {
    'INPUT': suitout,
    'PRJ_FILE_CREATE': True
}
processing.run('gdal:extractprojection', extpr_dict)
