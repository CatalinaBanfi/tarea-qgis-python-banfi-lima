        ## En este modelo vamos a utilizar los shapefile "ne_10m_admin_0_countries" y "ne_10m_coastline", con las fronteras y las costas de los países,
        ## obtenidos de Natural Earth Data, para poder finalizar el proceso con un archivo CSV con la distancia más corta desde el centroide del país hasta la costa.
        
        # Definimos las rutas para los inputs y los outputs del modelo.

        mainpath = "/Maestría UdeSA/Materias UdeSA/Herramientas computacionales/4. Python + GIS"
        inpath = "{}/input".format(mainpath)
        outpath = "{}/output".format(mainpath)
        
        admin_in = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(inpath)
        coast_in = "{}/ne_10m_coastline/ne_10m_coastline.shp".format(inpath)
        
        csvout = "{}/centroids_closest_coast.csv".format(outpath)
        
        # a) Cargamos el shapefile ne_10m_admin_0_countries, aplicando el algoritmo fix geometries.
        fg1_dict = {
            'INPUT': admin_in,
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', fg1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']
        
        # b) Cargamos el shapefile ne_10m_coastline, aplicando el algoritmo fix geometries.
        fg2_dict = {
            'INPUT': coast_in,
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['FixGeometriesCoast'] = processing.run('native:fixgeometries', fg2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['FixGeometriesCoast']['OUTPUT']
        
        # c) Aplicamos la función centroids a la layer de los países del punto a) para poder encontrar sus centroides.
        cts_dict = {
            'ALL_PARTS': False,
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'],
            'OUTPUT': parameters['Country_centroids']
        }
        outputs['Centroids'] = processing.run('native:centroids', cts_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']
        
        # d) Utilizamos la función add geometry attributes para obtener las coordenadas geográficas de los países del punto c).
        aga1_dict = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Centroids']['OUTPUT'],
            'OUTPUT': parameters['Centroids_w_coord']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', aga1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']
        
        # e) Usamos el algoritmo drop fields para determinar los campos con los que queremos quedarnos de la layer de b).
        df1_dict = {
            'COLUMN': ['scalerank'],
            'INPUT': outputs['FixGeometriesCoast']['OUTPUT'],
            'OUTPUT': parameters['Coastout']
        }
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', df1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']
        
        # f) Usamos el algoritmo drop fields para determinar los campos con los que queremos quedarnos de la layer de a).
        df2_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'],
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['DropFieldsCentroids_w_coord'] = processing.run('native:deletecolumn', df2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coord']['OUTPUT']
        
        # g) Aplicamos el algoritmo v.distance a las layer de los dos pasos anteriores, obteniendo el punto sobre la costa más cercano al centroide de cada país y su distancia.
        vd_dict = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['DropFieldsCentroids_w_coord']['OUTPUT'],
            'from_type': [0,1,3],  # point,line,area
            'to': outputs['DropFieldsFixgeo_coast']['OUTPUT'],
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', vd_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']
        
        # h) Utilizamos la función field calculator para ajustar el valor del atributo "cat" en la layer de los centroides más cercanos.
        fc1_dict = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature,'cat')-1",
            'INPUT': outputs['Vdistance']['from_output'],
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', fc1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']
        
        # i) Usamos el algoritmo drop fields para determinar los campos con los que queremos quedarnos de la layer de h). 
        df3_dict = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['FieldCalculatorCatAdjust']['OUTPUT'],
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['DropFieldsNearest_cat_adjust'] = processing.run('native:deletecolumn', df3_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsNearest_cat_adjust']['OUTPUT']
        
        # j) Realizamos un join en los atributos a través del valor de los campos para centroids y coast.
        jafv1_dict = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': outputs['DropFieldsCentroids_w_coord']['OUTPUT'],
            'INPUT_2': outputs['DropFieldsNearest_cat_adjust']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['JoinAttributesByFieldValueCentroidsYCoast'] = processing.run('native:joinattributestable', jafv1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT']
        
        # k) Usamos el algoritmo drop fields para determinar los campos con los que queremos quedarnos de la layer de j). 
        df4_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT'],
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['DropFieldsCentroids_nearest_coast_joined'] = processing.run('native:deletecolumn', df4_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroids_nearest_coast_joined']['OUTPUT']

        # l) Realizamos un join en los atributos para la tabla de más cercanos (ajustados) y la distancia.
        jafv2_dict = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': outputs['Vdistance']['output'],
            'INPUT_2': outputs['DropFieldsCentroids_nearest_coast_joined']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_distance_join']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', jafv2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_join'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        
        # m) Usamos el algoritmo extract vertices para extraer los vértices de la layer del paso anterior.
        ev_dict = {
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', ev_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']
        
        # n) Usamos el algoritmo extract by attribute para quedarnos solo con los vértices sobre las costas.
        eba_dict = {
            'FIELD': 'distance',
            'INPUT': outputs['ExtractVertices']['OUTPUT'],
            'OPERATOR': 2,  # >
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', eba_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']
        
        # o) Utilizamos la función field calculator para crear una variable con la latitud de los centroides.
        fc2_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': outputs['ExtractByAttribute']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', fc2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']
        
        # p) Utilizamos la función field calculator para crear una variable con la longitud de los centroides.
        fc3_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': outputs['FieldCalculatorCent_lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', fc3_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']
        
        # q) Usamos el algoritmo drop fields para determinar los campos con los que queremos quedarnos de la layer de p).
        df5_dict = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': outputs['FieldCalculatorCent_lon']['OUTPUT'],
            'OUTPUT': parameters['Centroids_lan_lon_dropfields']
        }
        outputs['DropFieldsAdded_field_cent_lon'] = processing.run('native:deletecolumn', df5_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lan_lon_dropfields'] = outputs['DropFieldsAdded_field_cent_lon']['OUTPUT']
        
        # r) Utilizamos la función add geometry attributes para obtener las coordenadas geográficas de puntos sobre la costa.
        aga2_dict = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['DropFieldsAdded_field_cent_lon']['OUTPUT'],
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AddGeometryAttributesCentroids_lan_lon_dropfields'] = processing.run('qgis:exportaddgeometrycolumns', aga2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributesCentroids_lan_lon_dropfields']['OUTPUT']
        
        # s) Utilizamos la función field calculator para crear una variable con la latitud de los puntos sobre la costa.
        fc4_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': outputs['AddGeometryAttributesCentroids_lan_lon_dropfields']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['FieldCalculatorAdd_geo_coast'] = processing.run('native:fieldcalculator', fc4_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorAdd_geo_coast']['OUTPUT']

        # t) Utilizamos la función field calculator para crear una variable con la longitud de los puntos sobre la costa.
        fc5_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': outputs['FieldCalculatorAdd_geo_coast']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', fc5_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']
        
        # u) Usamos la función drop fields para elegir los campos con los que nos queremos quedar y guardamos el resultado como archivo CSV.
        df6_dict = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['FieldCalculatorCoast_lon']['OUTPUT'],
            'OUTPUT': csvout,
        }
        outputs['DropFieldsAdded_field_coast_lon'] = processing.run('native:deletecolumn', df6_dict, context=context, feedback=feedback, is_child_algorithm=True)
     
