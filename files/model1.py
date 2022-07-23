# Para los scrips que siguen, necesitamos descargar sys, os y qgis
## Tambien QgsNativeAlgorithms
### En este script, trabajaremos sobre el shapefile WLMS

# Definimos las rutas para los inputs y los outputs del modelo
mainpath = "/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4"
wldsin = "{}/langa.shp".format(mainpath)
outpath = "{}/_output/".format(mainpath)
wldsout = "{}/wlds_cleaned.shp".format(outpath)

if not os.path.exists(outpath):
	os.mkdir(outpath)
    
 
##################################################################
# Fix geometries
##################################################################   
 # a) Utilizamos el algoritmo "fix geometries" en el shapefile langa
    
        lang_1 = {
            'INPUT': wldsin,
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', lang_1, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['FixGeometries']['OUTPUT']
 
 
##################################################################
# Add autoincremental field
##################################################################  
        
# b) Añadimos el campo ID autoincremental para los países
        ID_add = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', ID_add, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AddAutoincrementalField']['OUTPUT']        

##################################################################
# Calculadora de campos
##################################################################    
 # c) Usamos este algoritmo para limpiar la variable de aquellas con mas de 10
    
  fc_dict = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'lnm',
        'FIELD_PRECISION': 0,
        'FIELD_TYPE': 2,
        'FORMULA': ' attribute($currentfeature, \'NAME_PROP\')',
        'INPUT': outputs['AddAutoincrementalField']['OUTPUT'] ,
        'NEW_FIELD': True,
        'OUTPUT': 'memory:'
     }
         field_calc = processing.run('qgis:fieldcalculator', fc_dict)['OUTPUT']    


##################################################################
# Drop field(s)
################################################################## 
# d) Borramos los campos que no vamos a utilizar de la layer
        drp_1 = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': parameters['Wldsout']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', drp_1, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['DropFields']['OUTPUT']




