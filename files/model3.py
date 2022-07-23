#En este script, seleccionamos distintos rasters y les sacamos informacion para poder armar una tabla.
##Contamos con datos de elevacion, poblacion y landquality (archivo que generamos del model2)

 # Definimos las rutas para los inputs y los outputs del modelo
    
mainpath = "/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4"
outpath = "{}/_output".format(mainpath)

landqual = outpath + "/landquality.tif"
popd1800 = mainpath + "/1800ad_pop/1500ad_pop/popd_1500AD.asc"
popd1900 = mainpath + "/1900ad_pop/1990ad_pop/popd_1990AD.asc"
popd2000 = mainpath + "/2000ad_pop/2000ad_pop/popd_2000AD.asc"
countries = mainpath + "/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"

outcsv = "{}/raster_statics.csv".format(outpath)

   
##################################################################
# Corregir geometrias
##################################################################

# a) Utilizamos el algoritmo "fix geometries" en el shapefile ne_10m_admin_0_countries
        fg1_dict = {
            'INPUT': countries,
            'OUTPUT': parameters['Fix_geo_3']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', fg1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo_3'] = outputs['CorregirGeometras']['OUTPUT']


##################################################################
# Quitar campos
##################################################################

# b) Borramos campos que no vamos a utilizar de la layer creada en a)
        fg2_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': outputs['Fix_geo_3']['OUTPUT'],
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', fg2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['QuitarCampos']['OUTPUT']

    
##################################################################
# Estadisticas de zona por raster
##################################################################
# c) Usamos la funcion 'estadisticas' para quedarnos con la media de cada uno de los raster (lanq y popd..)
## Armamos un loop para facilitar el proceso

RASTS = [landqual, popd1500, popd1990, popd2000]
PREFS = ['lqua_', 'pd15_', 'pd19_', 'pd20_']

for idx, rast in enumerate(RASTS):

	pref = PREFS[idx]

    zs_dict = {
	    'COLUMN_PREFIX': pref,
	    'INPUT_RASTER': rast,
	    'INPUT_VECTOR': drop_fields,
	    'RASTER_BAND': 1,
	    'STATS': [2]
	}
	processing.run('qgis:zonalstatistics', zs_dict)
##################################################################
# Guardar registro en archivo .csv
##################################################################        
 
# Guardamos las estadisticas obtenidas en c) en un archivo .csv
       
with open(outcsv, 'w') as output_file:
    fieldnames = [field.name() for field in drop_fields_3.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in drop_fields_3.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)   

 
