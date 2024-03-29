        ## En este modelo vamos a utilizar el shapefile "ne_10m_admin_0_countries" con las fronteras de los países, obtenido 
        ## de Natural Earth Data, para armar un archivo CSV con el área en km2 de los países.

        # Definimos las rutas para los inputs y los outputs del modelo.
        
        mainpath = "/Maestría UdeSA/Materias UdeSA/Herramientas computacionales/4. Python + GIS"
        admin_in = "{}/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath)
        areas_out = "{}/output/areas.csv".format(mainpath)
        
        # a) Cargamos el shapefile ne_10m_admin_0_countries y eliminamos los campos con los que no deseamos trabajar.
        drop_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': admin_in,
            'OUTPUT': parameters['Countries_dropfields']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', drop_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_dropfields'] = outputs['DropFields']['OUTPUT']
        
        # b) Hacemos una reproyección cilíndrica del shapefile trabajado en el punto anterior, utilizando ESRI:54034.  
        reproj_dict = {
            'INPUT': outputs['DropFields']['OUTPUT'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'),
            'OUTPUT': parameters['Countries_reprojected']
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', reproj_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['ReprojectLayer']['OUTPUT']
        
        # c) Utilizamos el algoritmo "fix geometries" en la layer de los países reproyectados.
        fixgeo_dict = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': parameters['Countries_fixgeo']
        }
        outputs['FixGeometriesCountries_reprojected'] = processing.run('native:fixgeometries', fixgeo_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['FixGeometriesCountries_reprojected']['OUTPUT']
        
        # d) Utilizamos la función field calculator para realizar el cálculo del área de los países, en kilómetros cuadrados.
        fcalc_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'area($geometry)/1000000',
            'INPUT': outputs['FixGeometriesCountries_reprojected']['OUTPUT'],
            'OUTPUT': parameters['Areas_out']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', fcalc_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['FieldCalculator']['OUTPUT']

        # e) Guardamos el resultado en un archivo CSV.
        vftf_dict = {
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': areas_out
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', vftf_dict, context=context, feedback=feedback, is_child_algorithm=True)
