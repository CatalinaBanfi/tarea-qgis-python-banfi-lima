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
        
        # Field calculator - add_geo_coast
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': 'Added_geom_info_91a0e589_a917_4bee_9157_c7923afb90e9',
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['FieldCalculatorAdd_geo_coast'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorAdd_geo_coast']['OUTPUT']

        # Extract by attribute
        alg_params = {
            'FIELD': 'distance',
            'INPUT': 'Vertices_446464e7_125d_4647_972c_aaaa260712e9',
            'OPERATOR': 2,  # >
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']

        # Extract vertices
        alg_params = {
            'INPUT': 'Joined_layer_5cd04adb_383d_4e8c_99d0_5f0a7f0aec16',
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        # Add geometry attributes - centroids_lan_lon_dropfields
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': 'Remaining_fields_ccba3d8a_a95a_4d6d_b38d_5a69b99151c5',
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AddGeometryAttributesCentroids_lan_lon_dropfields'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributesCentroids_lan_lon_dropfields']['OUTPUT']

        # Field calculator - cent_lon
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': 'Calculated_c401105f_82ec_4424_9748_cc41208dac1a',
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']

        # Drop field(s) - added_field_cent_lon
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculated_248513d4_5ed2_499f_9c23_231cdaf66235',
            'OUTPUT': parameters['Centroids_lan_lon_dropfields']
        }
        outputs['DropFieldsAdded_field_cent_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lan_lon_dropfields'] = outputs['DropFieldsAdded_field_cent_lon']['OUTPUT']

        # Drop field(s) - fixgeo_coast
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Fixed_geometries_3590b732_8e19_4789_ac6d_c0cdd9f97228',
            'OUTPUT': parameters['Coastout']
        }
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']

        # Drop field(s) - nearest_cat_adjust
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_ab194c9c_a702_4c0e_a6fd_5af6d7c57249',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['DropFieldsNearest_cat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsNearest_cat_adjust']['OUTPUT']

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': 'output_1531b682_0aa2_4858_b5c5_485a6f3b95f4',
            'INPUT_2': 'Remaining_fields_51815c5f_1f6e_4237_a06c_372bc3b13d8c',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_distance_join']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_join'] = outputs['JoinAttributesByFieldValue']['OUTPUT']

        # Drop field(s) - centroids_nearest_coast_joined
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Joined_layer_ffab525d_44ec_4ef4_97ee_6460283a26d8',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['DropFieldsCentroids_nearest_coast_joined'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroids_nearest_coast_joined']['OUTPUT']

        # Join attributes by field value - centroids y coast
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': 'Remaining_fields_f3aa8f95_9f23_43a1_ade6_b3f355387623',
            'INPUT_2': 'Remaining_fields_a198ecef_ed1d_4514_8775_67c6d6c29916',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['JoinAttributesByFieldValueCentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT']
        
        # Field calculator- cat adjust
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature,'cat')-1",
            'INPUT': 'from_output_2c8dd046_2558_47b2_87ec_ddf85d9dec12',
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']

        # Drop field(s) - centroids_w_coord
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Added_geom_info_448a073e_06ab_4742_849e_cb1a0ff58d5f',
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['DropFieldsCentroids_w_coord'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coord']['OUTPUT']

        # Drop field(s) - added_field_coast_lon
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_e14fb4d2_74e3_4ba4_b33a_156b7d5485eb',
            'OUTPUT': 'C:/Maestría UdeSA/Materias UdeSA/Herramientas computacionales/4. Python + GIS/output/csvout.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFieldsAdded_field_coast_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Field calculator - coast_lon
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': 'Calculated_fc223fb0_06fb_4b03_a020_589e74656025',
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']

        # Field calculator - cent_lat
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': 'Extracted__attribute__8111e623_5613_4299_90fa_34e24ed31ddb',
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']

        # v.distance
        alg_params = {
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
            'from': 'Remaining_fields_f3aa8f95_9f23_43a1_ade6_b3f355387623',
            'from_type': [0,1,3],  # point,line,area
            'to': 'Remaining_fields_ca89cfd8_9077_409e_8098_c01a5a2c0ae2',
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Centroids']['OUTPUT'],
            'OUTPUT': parameters['Centroids_w_coord']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']
       
